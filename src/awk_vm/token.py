class TokenType:
    NewObject = 0
    Equal = 1
    LessThan = 2
    GreaterThan = 3
    Plus = 4
    Dot = 5
    Identity = 6
    Literal = 7
    End = 7
    While = 9
    BodyStart = 10
    BodyEnd = 11
    Condition = 12


class Token:
    token = -1
    value = ""
    numericValue = 0
    prop = ""
    condition = []
    body = []

    def __init__(
        self, token, literalValue, prop="", numericValue=0, condition=[], body=[]
    ):
        self.token = token
        self.value = literalValue
        self.prop = prop
        self.numericValue = numericValue
        self.condition = condition
        self.body = body

    def __str__(self):
        return (
            "(Token:["
            + self.token
            + "], Value:["
            + self.value
            + "], Prop:["
            + self.prop
            + "], NumericValue:["
            + str(self.numericValue)
            + "])"
        )
