from __future__ import annotations

from benchmark import run


def main() -> None:
    payload = run(quick=True)
    print(f"Training benchmark completed with backend={payload['backend']}")


if __name__ == "__main__":
    main()
