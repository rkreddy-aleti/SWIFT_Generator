def generate_mt548(data):
    return (
        f":20:{data['Transaction Ref']}\n"
        f":25D::{data['Status']}\n"
        f":98A::PROC//{data['Processing Time']}\n"
        "-\n"
    )
