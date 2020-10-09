import converters.bank1 as bank1
import converters.bank2 as bank2
import converters.bank3 as bank3

TESTS = {"bank1": bank1.test, "bank2": bank2.test, "bank3": bank3.test}

CONVERTERS = {"bank1": bank1.convert, "bank2": bank2.convert, "bank3": bank3.convert}
