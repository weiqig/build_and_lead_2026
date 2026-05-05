import sys
from src import Ingestor, Processor, Loader, Profiler

def display_help(command_list: list) -> None:
    print("commands: ", end='')
    print(", ".join(command_list))


def main() -> None:
    command_list =['ingest', 'process', 'clean']

    if len(sys.argv) < 2:
        print("Usage: python main.py <command> <process_amount (optional)>")
        display_help(command_list)
        return

    if len(sys.argv) == 3:
        if sys.argv[2] and isinstance(sys.argv[2], int):
            try:
                process_amount = int(sys.argv[2])
            except Exception:
                print("Invalid input. Please enter a valid integer")
            ingestor = Ingestor(process_amount)
        else:
            ingestor = Ingestor()
    else:
        ingestor = Ingestor()
    processor = Processor()
    loader = Loader()
    profiler = Profiler()
    command = sys.argv[1]
    match command:
        case 'ingest':
            ingestor.ingest()
        case 'process':
            processor.process()
        case 'load':
            loader.load()
        case 'profile':
            profiler.profile()
        case 'all':
            ingestor.ingest()
            processor.process()
            loader.load()
            profiler.profile()
        case 'clean':
            if len(sys.argv) == 3:
                match sys.argv[2]:
                    case '1':
                        ingestor.clean()
                    case '2':
                        processor.clean()
                    case '3':
                        loader.delete_data()
                    case 'all':
                        ingestor.clean()
                        processor.clean()
                        loader.delete_data()
                    case _:
                        pass
            else:
                ingestor.clean()
        case _:
            print("Unknown command:", command)


if __name__ == "__main__":
    main()
