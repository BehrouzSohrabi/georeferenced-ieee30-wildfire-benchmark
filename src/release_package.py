"""Validate the georeferenced spatial release package."""
import hashlib
import json
import zipfile
from pathlib import Path

MANIFEST = Path("data/network/manifest.json")


def validate_release_manifest(root: Path) -> list[str]:
    root = Path(root)
    manifest = json.loads((root / MANIFEST).read_text(encoding="utf-8"))
    asset = manifest["asset"]
    relative = Path(asset["path"])
    errors: list[str] = []
    if relative.is_absolute() or ".." in relative.parts or relative.parts[0] == "sources":
        return [f"invalid release asset path: {relative.as_posix()}"]
    path = root / relative
    if not path.is_file():
        return [f"missing release asset: {relative.as_posix()}"]
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    if digest != asset["sha256"]:
        errors.append(f"checksum mismatch: {relative.as_posix()}")
    network = json.loads(path.read_text(encoding="utf-8"))
    if network.get("type") != "FeatureCollection":
        return errors + ["network is not a GeoJSON FeatureCollection"]
    features = network.get("features", [])
    points = [f for f in features if f.get("geometry", {}).get("type") == "Point"]
    lines = [f for f in features if f.get("geometry", {}).get("type") == "LineString"]
    if len(points) != asset["bus_point_count"]:
        errors.append("bus point count mismatch")
    if len(lines) != asset["branch_route_count"]:
        errors.append("branch route count mismatch")
    bus_ids = {f.get("properties", {}).get("bus") for f in points}
    if bus_ids != set(range(1, asset["bus_point_count"] + 1)):
        errors.append("bus identifiers are not the complete 1..N set")
    for index, feature in enumerate(features, start=1):
        if feature.get("geometry", {}).get("type") != "LineString":
            continue
        props = feature.get("properties", {})
        if not all(isinstance(props.get(k), int) and not isinstance(props.get(k), bool) for k in ("branch", "fbus", "tbus")):
            errors.append(f"line feature {index} missing integer endpoint properties")
    return errors


def _sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def validate_release_archive(root: Path) -> list[str]:
    """Verify the exact archive, its embedded manifest, and current source assets."""
    root = Path(root)
    manifest_path = root / "dist/release-manifest.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest = json.loads(manifest_bytes)
    archive = root / "dist" / manifest["release_name"]
    errors: list[str] = []
    expected = {item["path"]: item["sha256"] for item in manifest["assets"]}
    if len(expected) != len(manifest["assets"]):
        errors.append("duplicate asset path in release manifest")
    if not archive.is_file():
        return ["release archive is missing"]

    sums = root / "dist/SHA256SUMS"
    expected_sum_line = f"{_sha256_bytes(archive.read_bytes())}  {archive.name}"
    if not sums.is_file() or sums.read_text(encoding="utf-8").strip() != expected_sum_line:
        errors.append("outer archive checksum mismatch")

    for path, digest in expected.items():
        source = root / path
        if not source.is_file():
            errors.append("missing root asset: " + path)
        elif _sha256_bytes(source.read_bytes()) != digest:
            errors.append("root asset checksum mismatch: " + path)

    with zipfile.ZipFile(archive) as handle:
        member_names = handle.namelist()
        names = set(member_names)
        if len(names) != len(member_names):
            errors.append("duplicate archive member")
        forbidden = [n for n in names if any(x in n.lower() for x in ("farsite", "pypower", "matpower", "sources/"))]
        if forbidden:
            errors.append("restricted member: " + forbidden[0])
        for path, digest in expected.items():
            if path not in names:
                errors.append("missing member: " + path)
            elif _sha256_bytes(handle.read(path)) != digest:
                errors.append("member checksum mismatch: " + path)
        if "release-manifest.json" not in names:
            errors.append("missing member: release-manifest.json")
        elif handle.read("release-manifest.json") != manifest_bytes:
            errors.append("embedded release manifest mismatch")

    allowed = set(expected) | {"release-manifest.json"}
    for path in sorted(names - allowed):
        errors.append("unexpected member: " + path)
    return errors
