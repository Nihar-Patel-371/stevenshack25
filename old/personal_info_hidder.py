from presidio_analyzer import AnalyzerEngine, PatternRecognizer, Pattern, RecognizerResult
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
from pprint import pprint
import json
import re

text_to_anonymize = '''I am Nihar Patel, and I am a MS Data Science student at Stevens Institute of Technology, I have my phone number +1(341) 927 9456, 3419279456.

My socials are 13348948, and I am currently living at 1234, 5th Avenue, New York, NY 10001, 401 6th ST, Union City.
I am pasting my resume below for your reference:

'''

if __name__ == "__main__":

    # Initialize Presidio Analyzer and Anonymizer
    analyzer = AnalyzerEngine()
    anonymizer = AnonymizerEngine()

    # Custom SSN Recognizer (Matches US SSN format: XXX-XX-XXXX)
    ssn_pattern = Pattern(name="SSN (US)", regex=r"\b\d{3}-\d{2}-\d{4}\b", score=0.9)
    ssn_recognizer = PatternRecognizer(supported_entity="US_SSN", patterns=[ssn_pattern])

    # Custom Address Recognizer (Basic Address Pattern Example)
    address_pattern = Pattern(name="Address", regex=r"\b\d{1,5}\s\w+(\s\w+)*\s(St|Ave|Blvd|Rd|Ln|Dr|Ct)\b", score=0.5)
    address_recognizer = PatternRecognizer(supported_entity="ADDRESS", patterns=[address_pattern])

    # Add Custom Recognizers to Analyzer
    analyzer.registry.add_recognizer(ssn_recognizer)
    analyzer.registry.add_recognizer(address_recognizer)

    def anonymize_text(text_to_anonymize):
        # Analyze text to identify PII entities
        results = analyzer.analyze(text=text_to_anonymize, entities=["PHONE_NUMBER", "ADDRESS", "US_SSN"], language="en")

        # Define anonymization strategy (replace with placeholders)
        anonymizer_config = {
            "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "XXX-XXX-XXXX"}),
            "ADDRESS": OperatorConfig("replace", {"new_value": "[REDACTED ADDRESS]"}),
            "US_SSN": OperatorConfig("replace", {"new_value": "XXX-XX-XXXX"})
        }

        # Apply anonymization
        anonymized_text = anonymizer.anonymize(text=text_to_anonymize, analyzer_results=results, operators=anonymizer_config)

        return anonymized_text.text

    # Example usage
    text_to_anonymize = "John's phone number is 555-273-4590 and his SSN is 123-45-6789. He lives at 123 Main St, New York."
    anonymized_text = anonymize_text(text_to_anonymize)
    print(anonymized_text)