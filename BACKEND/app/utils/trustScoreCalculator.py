def calculate_trust_score(
    qr_match: bool,
    batch_match: bool,
    scan_count: int,
    manufacturer_verified: bool = True,
) -> int:
    score = 0

    # 1. QR / Barcode verification
    if qr_match:
        score += 40

    # 2. Batch number verification
    if batch_match:
        score += 25

    # 3. Manufacturer verification
    if manufacturer_verified:
        score += 20

    # 4. Suspicious repeated scans
    if scan_count <= 20:
        score += 15
    elif scan_count <= 50:
        score += 7
    else:
        score += 0

    return min(score, 100)