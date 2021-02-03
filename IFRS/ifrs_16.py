import numpy as np


class IFRS_16:

    def __init__(self, interestRate, compoundingFrequency, periodicCashFlow, futureValue, numberOfYears, when):
        self.interestRate = interestRate
        self.compoundingFrequency = compoundingFrequency
        self.periodicCashFlow = periodicCashFlow
        self.futureValue = futureValue  # Prob need to default xero
        self.numberOfYears = numberOfYears
        self.when = when
        self.initial_recognition = self.initial_recognition_amount()
        # self.startdate = startdate

    def initial_recognition_amount(self):
        """Get aount of lease at initial recognition

        Args:
            self

        Returns:
            float: PV of cashflows for lease payments to be recognised on the balancesheet
        """
        return np.pv(self.interestRate/self.compoundingFrequency, self.compoundingFrequency*self.numberOfYears, self.periodicCashFlow, self.futureValue, self.when)

    def depreciation_amount(self, method='straight_line'):
        if method == "straight_line":
            return self.initial_recognition / self.numberOfYears

    def journal(self, startdate):
        reducing_balance = self.initial_recognition
        entries = []
        while reducing_balance > 0:
            interest_payable = reducing_balance * self.interestRate
            lease_liability = - self.periodicCashFlow - interest_payable
            reducing_balance -= lease_liability

            entries.append({"period": startdate, "debit/credit": "dr",
                            "account": "interest_payable", "amount": interest_payable})

            if reducing_balance < lease_liability:
                break

        print(entries)
