import re
from uuid import uuid4


# standard Google Translate API Basic function
def translate(source, target, text):
    """Translates text into the target language.

    Target must be an ISO 639-1 language code.
    See https://g.co/cloud/translate/v2/translate-reference#supported_languages
    """
    import six
    from google.cloud import translate_v2 as translate

    translate_client = translate.Client.from_service_account_json(
        "keys/localizse-18660e5baf67.json"
    )

    if isinstance(text, six.binary_type):
        text = text.decode("utf-8")

    # Text can also be a sequence of strings, in which case this method
    # will return a sequence of results for each text.
    result = translate_client.translate(
        text, source_language=source, target_language=target, format_="text"
    )

    return result["translatedText"]


# a version of the translation to deal with tech content
def tech_translate(source, target, text):
    factored = text
    # replaces the latex with uuid and records the mapping
    snip_map = [
        (m, str(uuid4())) for m in set(re.findall(r"\${1,2}.+?\${1,2}", factored))
    ]

    for snip in snip_map:
        factored = factored.replace(snip[0], snip[1])
    # translating with the uuids included, then replacing the latex back in.
    translated = translate(source, target, factored)
    for snip in snip_map:
        translated = translated.replace(snip[1], snip[0])
    return translated
