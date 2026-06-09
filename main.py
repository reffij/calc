from calculator import calculate

def main() -> None:
    while True:
        response = input("Write your expression (Q to quit): ")
        if response.upper() == 'Q':
            break
        try:
            print(f"ans: {calculate(response)}")
        except Exception as e:
            print(f"[ERROR] {e}")

if __name__ == '__main__':
    main()