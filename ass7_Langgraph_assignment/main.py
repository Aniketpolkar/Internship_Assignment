from graph import build_graph

def main():
    app = build_graph()

    initial_state = {
        "symptoms": None,
        "knowledge": None,
        "advice": None,
        "messages": []
    }

    final_state = app.invoke(initial_state)

    print("\n--- Clinical Advice ---")
    print(final_state["advice"])

    print("\n--- Debug Trace ---")
    for msg in final_state["messages"]:
        print("-", msg)

if __name__ == "__main__":
    main()
