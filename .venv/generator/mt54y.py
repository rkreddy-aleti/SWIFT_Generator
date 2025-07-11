def generate_mt54y(data):
    return (
        f":21:{data['Related Ref']}\n"
        f":70E:{data['Narrative']}\n"
        "-\n"
    )
