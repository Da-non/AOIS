def main():
    print("=== ЛАБОРАТОРНАЯ РАБОТА 2 ===")
    expr = input("Введите логическую функцию (a,b,c,d,e & | ! -> ~): ").strip()
    try:
        analyzer = BooleanAnalyzer(expr)
        analyzer.run_report()
    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    main()
