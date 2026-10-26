with open(r"C:\Users\vrohi\romflasher-site\dist\index.html", "r", encoding="utf-8") as f:
    text = f.read()

pos = text.find('class="card"')
print("Found pos:", pos)
if pos != -1:
    print(text[pos-20:pos+800])

# Also check bento cards
bpos = text.find('class="bento-card"')
print("\nBento pos:", bpos)
if bpos != -1:
    print(text[bpos-20:bpos+500])
