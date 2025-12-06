import json

FACTS_FILE = "../kb/facts.json"

# ------------------------------
# Rule representation
# ------------------------------

class Rule:
    def __init__(self, conditions, conclusion):
        """
        conditions: list of ("fact_type", var)
        conclusion: ("fact_type", var or value)
        Example:
           IF ("score", s) AND s > 24 THEN ("eligible", True)
        """
        self.conditions = conditions
        self.conclusion = conclusion

# ------------------------------
# Forward Chaining Engine
# ------------------------------

class ForwardChainingEngine:
    def __init__(self, facts, rules):
        self.facts = set(tuple(f) for f in facts)   # convert to set for fast lookup
        self.rules = rules
        self.inferred = set()

    def match_conditions(self, rule):
        """Check if rule's conditions are satisfied by facts"""
        for cond in rule.conditions:
            cond_type, cond_value = cond

            matched = False
            for fact in self.facts:
                fact_type = fact[0]
                fact_value = fact[1] if len(fact) > 1 else None

                if fact_type == cond_type:
                    # If cond_value is a bound variable, accept any match
                    matched = True
                    break

            if not matched:
                return False

        return True

    def infer(self):
        added_new = True

        while added_new:
            added_new = False

            for rule in self.rules:
                if self.match_conditions(rule):
                    new_fact = rule.conclusion
                    if new_fact not in self.facts:
                        print("New fact inferred:", new_fact)
                        self.facts.add(new_fact)
                        self.inferred.add(new_fact)
                        added_new = True

        return self.facts, self.inferred

# ------------------------------
# Example Rule Set
# ------------------------------

def example_rules():
    rules = []

    # Rule 1: If score >= 24 → eligible_for_CSE
    rules.append(
        Rule(
            conditions=[("score", None)],
            conclusion=("eligibility", "likely_admitted")
        )
    )

    # Rule 2: If method is 'xét học bạ' → requires transcript
    rules.append(
        Rule(
            conditions=[("method", None)],
            conclusion=("document_required", "học bạ")
        )
    )

    return rules

# ------------------------------
# Main
# ------------------------------

def main():
    with open(FACTS_FILE, "r", encoding="utf-8") as f:
        facts = json.load(f)

    rules = example_rules()
    engine = ForwardChainingEngine(facts, rules)
    all_facts, inferred = engine.infer()

    print("\nFINAL FACTS:")
    for f in all_facts:
        print("  ", f)

    print("\nNEWLY INFERRED FACTS:")
    for f in inferred:
        print("  ", f)

if __name__ == "__main__":
    main()
