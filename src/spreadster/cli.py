from __future__ import annotations
import argparse
from spreadster.config import Config

def main():
    parser = argparse.ArgumentParser(description="spreadster unified CLI")
    sub = parser.add_subparsers(dest="mode", required=True)

    p_daily = sub.add_parser("daily")
    p_daily.add_argument("--symbol", default="SPX")
    p_daily.add_argument("--sample", action="store_true")
    p_daily.add_argument("--with-openai", action="store_true")
    p_daily.add_argument("--with-telegram", action="store_true")

    p_live = sub.add_parser("live")
    p_live.add_argument("--sample", action="store_true")
    p_live.add_argument("--input")
    p_live.add_argument("--with-openai", action="store_true")
    p_live.add_argument("--with-telegram", action="store_true")

    p_cfg = sub.add_parser("config")
    p_cfg.add_argument("--print", action="store_true")

    args, rest = parser.parse_known_args()

    if args.mode == "config":
        print(Config.as_dict())
        Config.print_status()
        return

    if args.mode == "daily":
        from spreadster.main import main as daily_main
        import sys
        sys.argv = ["spreadster.main"]
        if args.symbol: sys.argv += ["--symbol", args.symbol]
        if args.sample: sys.argv += ["--sample"]
        if args.with_openai: sys.argv += ["--with-openai"]
        if args.with_telegram: sys.argv += ["--with-telegram"]
        daily_main()
        return

    if args.mode == "live":
        from spreadster.live.main import main as live_main
        import sys
        sys.argv = ["spreadster.live.main"]
        if args.sample: sys.argv += ["--sample"]
        if args.input: sys.argv += ["--input", args.input]
        if args.with_openai: sys.argv += ["--with-openai"]
        if args.with_telegram: sys.argv += ["--with-telegram"]
        live_main()
        return

if __name__ == "__main__":
    main()
