from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TrainingSummary:
    epochs: int
    teacher_forcing_steps: int
    mean_sequence_energy: float


def summarize_dataset(
    dataset: list[list[list[float]]], epochs: int, teacher_forcing_steps: int
) -> TrainingSummary:
    energies = []
    for sample in dataset:
        flat = [value for row in sample for value in row]
        energies.append(sum(value * value for value in flat) / len(flat))
    return TrainingSummary(
        epochs=epochs,
        teacher_forcing_steps=teacher_forcing_steps,
        mean_sequence_energy=sum(energies) / len(energies) if energies else 0.0,
    )
