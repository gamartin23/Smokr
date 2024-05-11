class TestCase:
    def __init__(self, id, name, android_state='Untested',ios_state="Untested", comments="", related_issues: list[str]=[]):
        self.id = id
        self.name = name
        self.android_state = android_state
        self.ios_state = ios_state
        self.comments = comments
        self.related_issues = related_issues