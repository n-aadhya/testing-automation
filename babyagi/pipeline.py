from babyagi.agent import BabyAGIAgent

def run():
    file_path = "src/max3.cpp"   # change dynamically later

    agent = BabyAGIAgent(file_path)
    agent.execute_pipeline()     # ✅ THIS is the key fix


if __name__ == "__main__":
    run()
