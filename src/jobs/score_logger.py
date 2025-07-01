from src.engines.score_engine import ScoreEngine

def main():
    try:
        engine = ScoreEngine()
        engine.run()
    except Exception as e:
        print(f"[SCORE_LOGGER] Error: {e}")

if __name__ == "__main__":
    main()

