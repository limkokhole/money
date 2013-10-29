"""
NOTES:
* binary operations try to convert currencies
* Division between two Money objects drops the currency
* Money objects are not hashable
* FIXME: bool() behaves just like Decimal. e.g. bool(Money(0, 'EUR')) --> False
"""
import locale
import logging
from decimal import Decimal


logger = logging.getLogger(__name__)


class Money(object):
    __hash__ = None
    
    def __init__(self, amount="0", currency=None):
        self.amount = Decimal(amount)
        self.currency = currency
    
    def __repr__(self):
        return "{} {}".format(self.currency, self.amount)
    
    def __str__(self):
        try:
            amount = locale.currency(self.amount, symbol=False, grouping=True, international=False)
            return "{} {}".format(amount, self.currency)
        except ValueError:
            return self.__repr__()
    
    def __lt__(self, other):
        return self.amount < self._get_amount(other)
    
    def __le__(self, other):
        return self.amount <= self._get_amount(other)
    
    def __eq__(self, other):
        return self.amount == self._get_amount(other)
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __gt__(self, other):
        return self.amount > self._get_amount(other)
    
    def __ge__(self, other):
        return self.amount >= self._get_amount(other)
    
    def __bool__(self):
        return bool(self.amount)
    
    def __add__(self, other):
        amount = self.amount + self._get_amount(other)
        return self.__class__(amount, self.currency)
    
    def __sub__(self, other):
        amount = self.amount - self._get_amount(other)
        return self.__class__(amount, self.currency)
    
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            raise TypeError("multiplication is unsupported between {} objects".format(self.__class__.__name__))
        amount = self.amount * other
        return self.__class__(amount, self.currency)
    
    def __truediv__(self, other):
        if isinstance(other, self.__class__):
            return self.amount / other.convert_to(self.currency).amount
        else:
            amount = self.amount / other
            return self.__class__(amount, self.currency)
    
    def __floordiv__(self, other):
        if isinstance(other, self.__class__):
            return self.amount // other.convert_to(self.currency).amount
        else:
            amount = self.amount // other
            return self.__class__(amount, self.currency)
    
    def __mod__(self, other):
        if isinstance(other, self.__class__):
            raise TypeError("modulo is unsupported between {} objects".format(self.__class__.__name__))
        amount = self.amount % other
        return self.__class__(amount, self.currency)
    
    def __divmod__(self, other):
        if isinstance(other, self.__class__):
            return divmod(self.amount, other.convert_to(self.currency).amount)
        whole, remainder = divmod(self.amount, other)
        return (self.__class__(whole, self.currency), self.__class__(remainder, self.currency))
    
    def __pow__(self, other):
        if isinstance(other, self.__class__):
            raise TypeError("power operator is unsupported between {} objects".format(self.__class__.__name__))
        amount = self.amount ** other
        return self.__class__(amount, self.currency)
    
    def __lshift__(self, other):
        return NotImplemented
    
    def __rshift__(self, other):
        return NotImplemented
    
    def __and__(self, other):
        return NotImplemented
    
    def __xor__(self, other):
        return NotImplemented
    
    def __or__(self, other):
        return NotImplemented
    
    def _get_amount(self, other):
        """Return the converted amount of the other, if possible."""
        if isinstance(other, self.__class__):
            return other.convert_to(self.currency).amount
        else:
            return other
    
    def convert_to(self, currency):
        if currency == self.currency:
            return self
        else:
            raise NotImplementedError("Money exchange not implemented yet")





