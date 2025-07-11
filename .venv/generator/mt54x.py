import os

def generate_mt54x(data, mt_type):
    return f"""{{1:F01{data['Sender BIC']}XXXX0000000000}}
{{2:I{mt_type[-3:]}{data['Receiver BIC']}XXXXN}}
{{4:
:16R:GENL
:20C::SEME//{data['Transaction Ref']}
:23G:{data['Function of Message']}
:98A::PREP//{data['Preparation Date']}
:16S:GENL
:16R:TRADDET
:98A::TRAD//{data['Trade Date']}
:98A::SETT//{data['Settlement Date']}
:90B::DEAL//ACTU/{data['Currency']}{data['Deal Price']}
:35B:{data['ISIN']}
:16S:TRADDET
:16R:SETDET
:22F::SETR//{data['Settlement Transaction Indicator']}
:95P::BUYR//{data['Buyer BIC']}
:95P::SELL//{data['Seller BIC']}
:16S:SETDET
-}}"""

def generate_mt548_from_mt54x(content, status):
    try:
        sender = content.split("{1:F01")[1].split("XXXX")[0]
        receiver = content.split("{2:I")[1][3:15]
        ref = next(line for line in content.splitlines() if ":20C::SEME//" in line).split("//")[1]
    except Exception:
        return "Invalid MT54x format for MT548 generation."

    return f"""{{1:F01{sender}XXXX0000000000}}
{{2:I548{receiver}XXXXN}}
{{4:
:20C::SEME//{ref}
:23G:STAT
:25D::PROC//{status}
-}}"""

def generate_mt54y_from_mt54x(content, settlement_type):
    try:
        sender = content.split("{1:F01")[1].split("XXXX")[0]
        receiver = content.split("{2:I")[1][3:15]
        ref = next(line for line in content.splitlines() if ":20C::SEME//" in line).split("//")[1]
    except Exception:
        return "Invalid MT54x format for MT54Y generation."

    return f"""{{1:F01{sender}XXXX0000000000}}
{{2:I54Y{receiver}XXXXN}}
{{4:
:20C::SEME//{ref}
:23G:REPO
:70E::INFO//Settlement Type: {settlement_type}
-}}"""

def save_message(content, filename):
    folder = "generated_messages"
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, filename)
    with open(path, "w") as file:
        file.write(content)
    return path
