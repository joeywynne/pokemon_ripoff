def normalise_vector(vector: tuple[float, float]) -> tuple[float, float]:
    """Return a normalized version of the vector."""
    x, y = vector
    magnitude = (x**2 + y**2) ** 0.5
    if magnitude == 0:
        return (0, 0)
    return (x / magnitude, y / magnitude)
