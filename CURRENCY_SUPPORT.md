# 💱 Multi-Currency Support

## Overview

The dashboard now **automatically detects** your Stripe account's currency and displays all amounts with the correct currency symbol.

---

## ✅ Supported Currencies

The system supports **30+ currencies** with their native symbols:

| Currency | Symbol | Example |
|----------|--------|---------|
| USD | $ | $1,234.56 |
| EUR | € | €1.234,56 |
| GBP | £ | £1,234.56 |
| JPY | ¥ | ¥123,456 |
| CAD | CA$ | CA$1,234.56 |
| AUD | A$ | A$1,234.56 |
| CHF | CHF | CHF1,234.56 |
| CNY | ¥ | ¥1,234.56 |
| INR | ₹ | ₹1,234.56 |
| MXN | MX$ | MX$1,234.56 |
| BRL | R$ | R$1.234,56 |
| ZAR | R | R1,234.56 |
| SEK | kr | 1,234.56 kr |
| NOK | kr | 1,234.56 kr |
| DKK | kr | 1,234.56 kr |
| PLN | zł | 1.234,56 zł |
| CZK | Kč | 1.234,56 Kč |
| HUF | Ft | 1.234,56 Ft |
| RUB | ₽ | ₽1,234.56 |
| TRY | ₺ | ₺1.234,56 |
| SGD | S$ | S$1,234.56 |
| HKD | HK$ | HK$1,234.56 |
| NZD | NZ$ | NZ$1,234.56 |
| KRW | ₩ | ₩1,234,567 |
| THB | ฿ | ฿1,234.56 |
| MYR | RM | RM1,234.56 |
| PHP | ₱ | ₱1,234.56 |
| IDR | Rp | Rp1,234,567 |
| AED | د.إ | د.إ1,234.56 |
| SAR | ﷼ | ﷼1,234.56 |

And more...

---

## 🔍 How It Works

### Backend Detection:
1. Fetches charges from your Stripe account
2. Identifies the currency of successful charges
3. Filters all data (charges, balance, payouts) by that currency
4. Returns the currency code (e.g., "GBP", "USD") in the API response

### Frontend Display:
1. Receives the currency from backend
2. Maps currency code to symbol (e.g., "GBP" → "£")
3. Formats all amounts with the correct symbol
4. Shows currency code in parentheses (e.g., "Balance (GBP)")

---

## 📊 Where Currency is Displayed

The dynamic currency is used in:

- ✅ **Payment Stats** - Succeeded, Uncaptured, Refunded, Blocked, Failed
- 💰 **Balance** - Available and Pending amounts
- 📅 **Next Payout** - Upcoming payout amount
- 📈 **Gross Volume Graph** - Tooltip hover amounts
- 📊 **Net Volume Graph** - Tooltip hover amounts

---

## 🎯 Examples

### USD Account:
```
💰 Balance (USD)
$1,234.56
Pending: $567.89

📅 Next Payout (USD)
$2,500.00
2025-11-30
```

### GBP Account:
```
💰 Balance (GBP)
£1,234.56
Pending: £567.89

📅 Next Payout (GBP)
£2,500.00
2025-11-30
```

### EUR Account:
```
💰 Balance (EUR)
€1.234,56
Pending: €567,89

📅 Next Payout (EUR)
€2.500,00
2025-11-30
```

---

## 🔧 Technical Notes

- **Backend**: Filters all Stripe data by detected currency
- **Multi-currency accounts**: Uses the currency of the first successful charge found
- **No charges**: Defaults to USD
- **Balance filtering**: Only shows balance for the detected currency
- **Payout filtering**: Only shows payouts in the detected currency

---

## 🚀 Benefits

1. ✅ **Automatic** - No configuration needed
2. 🌍 **Global** - Works with any Stripe-supported currency
3. 📊 **Accurate** - All amounts in the same currency
4. 🎨 **Native** - Shows proper currency symbols
5. 🔒 **Safe** - Prevents mixing different currencies

---

**Last Updated:** November 26, 2025

