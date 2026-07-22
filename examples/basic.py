from aftercare import Aftercare

order = []
with Aftercare() as ac:
    ac.add(lambda: order.append("close_db"), name="close_db")
    ac.add(lambda: order.append("flush_cache"), name="flush_cache")
    # main work...

assert order == ["flush_cache", "close_db"]
assert all(r.ok for r in ac.results)
print("aftercare ok", order)
