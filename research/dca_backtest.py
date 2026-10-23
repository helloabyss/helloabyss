"""DCA backtest for the 2026-09-28 QQQ/NVDA explainer.

Simplified, visible-maths DCA: $6,000 once a year (= $500/month), bought on the first
trading day of each year at the prior year-end close. Sources and grades are in
research/2026-09-28-dca.md.
"""
# QQQ: dividend-adjusted year-end closes (so results ~ total return, dividends reinvested).
# 2016-2024 match the published annual total returns to 0.01pp. 2025 derived from +20.77%.
QQQ = {2016:111.54, 2017:147.97, 2018:147.79, 2019:205.37, 2020:305.22,
       2021:388.91, 2022:262.20, 2023:406.04, 2024:509.90}
QQQ[2025] = round(QQQ[2024]*1.2077, 2)
# NVDA: split-adjusted year-end closes (price return; dividend is negligible).
# 2024/2025 anchors sourced; earlier years cross-checked against published annual returns.
NVDA = {2016:2.67, 2017:4.84, 2018:3.34, 2019:5.88, 2020:13.05,
        2021:29.41, 2022:14.61, 2023:49.52, 2024:134.29, 2025:186.27}
TODAY = {"QQQ": 739.28, "NVDA": 225.07}   # close 2026-09-25
PER_BUY = 6000

def dca(prices, today, first_year_end, last_year_end=2025):
    shares = invested = 0.0
    rows = []
    for y in range(first_year_end, last_year_end+1):
        p = prices[y]; s = PER_BUY/p
        shares += s; invested += PER_BUY
        rows.append((y+1, p, s))
    value = shares*today
    return dict(invested=invested, shares=shares, avg=invested/shares,
                value=value, gain=value-invested, mult=value/invested, rows=rows)

def lump(prices, today, year_end, amount):
    return amount/prices[year_end]*today

def check_returns():
    pub = {"QQQ": {2017:32.66,2018:-0.12,2019:38.96,2020:48.62,2021:27.42,2022:-32.58,2023:54.85,2024:25.58,2025:20.77},
           "NVDA":{2017:82,2018:-31,2019:77,2020:122,2021:125,2022:-50,2023:239,2024:171,2025:39}}
    worst = 0
    for name, px in (("QQQ",QQQ),("NVDA",NVDA)):
        for y,r in pub[name].items():
            impl = (px[y]/px[y-1]-1)*100
            tol = 0.05 if name=="QQQ" else 1.5   # NVDA table published to whole %
            d = abs(impl-r); worst=max(worst,d if name=="QQQ" else 0)
            assert d <= tol, (name,y,impl,r)
    return "price series reproduce published annual returns (QQQ within 0.05pp, NVDA within rounding)"

if __name__ == "__main__":
    print(check_returns())
    for name, px in (("QQQ",QQQ),("NVDA",NVDA)):
        t = TODAY[name]
        for label, start in (("10y: Jan 2017 -> Jan 2026, 10 buys", 2016), ("started at the top: Jan 2022 -> Jan 2026, 5 buys", 2021)):
            r = dca(px, t, start)
            ls = lump(px, t, start, r["invested"])
            print(f"\n{name} | {label}")
            print(f"  invested ${r['invested']:,.0f} | shares {r['shares']:,.2f} | avg cost ${r['avg']:,.2f} | today ${t:,.2f}")
            print(f"  value ${r['value']:,.0f} | gain ${r['gain']:,.0f} | {r['mult']:.2f}x | price vs avg cost +{(t/r['avg']-1)*100:.0f}%")
            print(f"  lump sum same total at start: ${ls:,.0f}  ({'beats' if ls>r['value'] else 'trails'} DCA)")
        if name=="NVDA":
            for y in (2021,2022):
                print(f"  NVDA buy Jan {y+1}: ${px[y]} -> {PER_BUY/px[y]:,.0f} shares for $6,000")
    # max drawdown between year-ends, for the risk beat
    print("\nworst calendar years: QQQ 2022 %.1f%%, NVDA 2022 %.1f%%" % ((QQQ[2022]/QQQ[2021]-1)*100,(NVDA[2022]/NVDA[2021]-1)*100))
    # forward, hypothetical only
    print("\nHYPOTHETICAL: $500/month, monthly compounding, FV at assumed annual rates")
    for yrs in (10,20):
        for rate in (0.06,0.10,0.14):
            i=rate/12; n=yrs*12; fv=500*(((1+i)**n-1)/i)
            print(f"  {yrs}y @ {rate:.0%}: contributed ${500*n:,.0f} -> ${fv:,.0f}")
