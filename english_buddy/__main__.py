import sys

from .cli import console, display_response, get_input, show_spinner
from .config import GEMINI_API_KEY
from .llm import create_client, query


def main():
    if not GEMINI_API_KEY:
        console.print("[red]Error: GEMINI_API_KEY not set. Copy .env.example to .env and fill in your key.[/red]")
        sys.exit(1)

    client = create_client()

    # Single-shot mode: python -m english_buddy "场景描述"
    if len(sys.argv) > 1:
        scene = " ".join(sys.argv[1:])
        with show_spinner():
            resp = query(scene, client)
        display_response(resp)
        return

    # Interactive mode
    console.print("[bold]English Buddy[/bold] - 输入中文场景描述，输入 quit 退出\n")
    while True:
        try:
            scene = get_input().strip()
            if scene.lower() in ("quit", "exit", "q"):
                break
            if not scene:
                continue
            with show_spinner():
                resp = query(scene, client)
            display_response(resp)
        except KeyboardInterrupt:
            break
        except Exception as e:
            console.print(f"[red]Error: {e}[/red]\n")

    console.print("\nBye!")


if __name__ == "__main__":
    main()
