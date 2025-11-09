"""Performance benchmarks for Rüsselsheim Chatbot."""

import asyncio
import time
import statistics
from typing import List, Dict
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.services.rag_service import RAGService
from app.services import weather_service, maps_service, traffic_service, holidays_service
from app.services.api_helper import detect_api_intent
from app.db.database import SessionLocal


class BenchmarkResults:
    """Container for benchmark results."""

    def __init__(self, name: str):
        self.name = name
        self.times: List[float] = []

    def add(self, duration: float):
        """Add a measurement."""
        self.times.append(duration)

    def summary(self) -> Dict[str, float]:
        """Calculate summary statistics."""
        if not self.times:
            return {}

        return {
            "count": len(self.times),
            "mean": statistics.mean(self.times),
            "median": statistics.median(self.times),
            "min": min(self.times),
            "max": max(self.times),
            "p95": sorted(self.times)[int(len(self.times) * 0.95)] if len(self.times) > 1 else self.times[0],
            "p99": sorted(self.times)[int(len(self.times) * 0.99)] if len(self.times) > 1 else self.times[0],
        }

    def print_summary(self):
        """Print formatted summary."""
        summary = self.summary()
        if not summary:
            print(f"{self.name}: No data")
            return

        print(f"\n{'='*60}")
        print(f"Benchmark: {self.name}")
        print(f"{'='*60}")
        print(f"  Samples:    {summary['count']}")
        print(f"  Mean:       {summary['mean']*1000:.2f} ms")
        print(f"  Median:     {summary['median']*1000:.2f} ms")
        print(f"  Min:        {summary['min']*1000:.2f} ms")
        print(f"  Max:        {summary['max']*1000:.2f} ms")
        print(f"  P95:        {summary['p95']*1000:.2f} ms")
        print(f"  P99:        {summary['p99']*1000:.2f} ms")


async def benchmark_weather_api(iterations: int = 10) -> BenchmarkResults:
    """Benchmark weather API calls."""
    results = BenchmarkResults("Weather API")

    for _ in range(iterations):
        start = time.time()
        await weather_service.get_weather()
        duration = time.time() - start
        results.add(duration)

    return results


async def benchmark_geocoding(iterations: int = 10) -> BenchmarkResults:
    """Benchmark geocoding API calls."""
    results = BenchmarkResults("Geocoding API")

    queries = ["Rüsselsheim", "Mainz", "Frankfurt", "Wiesbaden", "Darmstadt"]

    for i in range(iterations):
        query = queries[i % len(queries)]
        start = time.time()
        await maps_service.geocode_address(query)
        duration = time.time() - start
        results.add(duration)

    return results


async def benchmark_traffic_service(iterations: int = 10) -> BenchmarkResults:
    """Benchmark traffic/speed camera queries."""
    results = BenchmarkResults("Traffic Service (Speed Cameras)")

    # Rüsselsheim coordinates
    lat, lon = 49.9897, 8.4189

    for _ in range(iterations):
        start = time.time()
        await traffic_service.get_speed_cameras(lat, lon, radius=10000)
        duration = time.time() - start
        results.add(duration)

    return results


async def benchmark_holidays_api(iterations: int = 10) -> BenchmarkResults:
    """Benchmark holidays API calls."""
    results = BenchmarkResults("Holidays API")

    for _ in range(iterations):
        start = time.time()
        await holidays_service.get_next_holiday()
        duration = time.time() - start
        results.add(duration)

    return results


def benchmark_intent_detection(iterations: int = 1000) -> BenchmarkResults:
    """Benchmark intent detection (keyword matching)."""
    results = BenchmarkResults("Intent Detection")

    queries = [
        "Wie ist das Wetter?",
        "Wo liegt das Restaurant?",
        "Gibt es Blitzer auf der B43?",
        "Wann fährt der nächste Bus?",
        "Ist morgen ein Feiertag?",
        "Hallo, wie geht es dir?",
    ]

    for i in range(iterations):
        query = queries[i % len(queries)]
        start = time.time()
        detect_api_intent(query)
        duration = time.time() - start
        results.add(duration)

    return results


def benchmark_embedding_generation(iterations: int = 10) -> BenchmarkResults:
    """Benchmark embedding generation."""
    results = BenchmarkResults("Embedding Generation (384-dim)")

    db = SessionLocal()
    rag = RAGService(db)

    texts = [
        "Um einen Personalausweis zu beantragen, gehen Sie zum Bürgerbüro.",
        "Das Rathaus befindet sich in der Stadtmitte von Rüsselsheim.",
        "Die Öffnungszeiten sind Montag bis Freitag von 8 bis 16 Uhr.",
        "Für die Anmeldung benötigen Sie einen Termin.",
        "Der nächste Feiertag ist Weihnachten am 25. Dezember.",
    ]

    for i in range(iterations):
        text = texts[i % len(texts)]
        start = time.time()
        rag.embedding_service.create_embedding(text)
        duration = time.time() - start
        results.add(duration)

    db.close()
    return results


async def run_all_benchmarks():
    """Run all benchmarks and print results."""
    print("\n" + "="*60)
    print("PERFORMANCE BENCHMARKS - Rüsselsheim Chatbot")
    print("="*60)

    # Sync benchmarks
    print("\n[1/6] Intent Detection (sync)...")
    result = benchmark_intent_detection(iterations=1000)
    result.print_summary()

    print("\n[2/6] Embedding Generation (sync)...")
    result = benchmark_embedding_generation(iterations=10)
    result.print_summary()

    # Async benchmarks
    print("\n[3/6] Weather API (async)...")
    result = await benchmark_weather_api(iterations=5)
    result.print_summary()

    print("\n[4/6] Geocoding API (async)...")
    result = await benchmark_geocoding(iterations=5)
    result.print_summary()

    print("\n[5/6] Traffic Service (async)...")
    result = await benchmark_traffic_service(iterations=10)
    result.print_summary()

    print("\n[6/6] Holidays API (async)...")
    result = await benchmark_holidays_api(iterations=5)
    result.print_summary()

    print("\n" + "="*60)
    print("BENCHMARK COMPLETE")
    print("="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(run_all_benchmarks())
