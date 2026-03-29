import uuid

import pytest

LIST_PATHS = [
    "/admin/merchants",
    "/admin/users",
    "/admin/shops",
    "/admin/rooms",
    "/admin/room-orders",
    "/admin/order-discounts",
    "/admin/user-auths",
]


@pytest.mark.asyncio
@pytest.mark.parametrize("path", LIST_PATHS)
async def test_list_returns_total_and_items(path, client):
    r = await client.get(path)
    assert r.status_code == 200
    payload = r.json()
    assert payload["code"] == 0
    data = payload["data"]
    assert isinstance(data["total"], int)
    assert data["total"] == 0
    assert data["items"] == []
    assert data["skip"] == 0
    assert data["limit"] == 20


@pytest.mark.asyncio
async def test_list_total_not_reduced_by_limit(client):
    for i in range(3):
        r = await client.post("/admin/merchants", json={"company_name": f"C{i}"})
        assert r.status_code == 200
    r = await client.get("/admin/merchants", params={"limit": 1, "skip": 0})
    data = r.json()["data"]
    assert data["total"] == 3
    assert len(data["items"]) == 1


@pytest.mark.asyncio
async def test_soft_deleted_excluded_from_list_and_get_by_default(client):
    c = await client.post("/admin/merchants", json={"company_name": "X"})
    assert c.status_code == 200
    mid = c.json()["data"]["id"]

    assert (await client.get("/admin/merchants")).json()["data"]["total"] == 1

    assert (await client.delete(f"/admin/merchants/{mid}")).status_code == 200

    r = await client.get("/admin/merchants")
    assert r.json()["data"]["total"] == 0
    assert r.json()["data"]["items"] == []

    assert (await client.get(f"/admin/merchants/{mid}")).status_code == 404
    assert (await client.patch(f"/admin/merchants/{mid}", json={"company_name": "Y"})).status_code == 404

    r_inc = await client.get("/admin/merchants", params={"include_deleted": True})
    assert r_inc.json()["data"]["total"] == 1

    g = await client.get(f"/admin/merchants/{mid}", params={"include_deleted": True})
    assert g.status_code == 200
    assert g.json()["data"]["company_name"] == "X"


@pytest.mark.asyncio
async def test_list_total_counts_only_non_deleted(client):
    await client.post("/admin/merchants", json={"company_name": "A"})
    b = await client.post("/admin/merchants", json={"company_name": "B"})
    bid = b.json()["data"]["id"]
    await client.delete(f"/admin/merchants/{bid}")
    r = await client.get("/admin/merchants")
    assert r.json()["data"]["total"] == 1
    r_all = await client.get("/admin/merchants", params={"include_deleted": True})
    assert r_all.json()["data"]["total"] == 2


@pytest.mark.asyncio
async def test_users_crud_list_total(client):
    assert (await client.get("/admin/users")).json()["data"]["total"] == 0
    p = await client.post("/admin/users", json={"nickname": "n1", "mobile": "13800000001"})
    assert p.status_code == 200
    assert (await client.get("/admin/users")).json()["data"]["total"] == 1


@pytest.mark.asyncio
async def test_shops_rooms_orders_discounts_auths(client):
    m = await client.post("/admin/merchants", json={"company_name": "Co"})
    mid = m.json()["data"]["id"]
    s = await client.post(
        "/admin/shops",
        json={"merchant_id": mid, "shop_name": "S1"},
    )
    assert s.status_code == 200
    sid = s.json()["data"]["id"]
    assert (await client.get("/admin/shops")).json()["data"]["total"] == 1

    rm = await client.post(
        "/admin/rooms",
        json={"shop_id": sid, "room_name": "R1", "room_type": "office"},
    )
    assert rm.status_code == 200
    rid = rm.json()["data"]["id"]
    assert (await client.get("/admin/rooms")).json()["data"]["total"] == 1

    u = await client.post("/admin/users", json={"nickname": "u1"})
    uid = u.json()["data"]["id"]

    on = f"O{uuid.uuid4().hex}"
    ro = await client.post(
        "/admin/room-orders",
        json={
            "order_number": on,
            "user_id": uid,
            "shop_id": sid,
            "room_id": rid,
        },
    )
    assert ro.status_code == 200
    oid = ro.json()["data"]["id"]
    assert (await client.get("/admin/room-orders")).json()["data"]["total"] == 1

    od = await client.post(
        "/admin/order-discounts",
        json={"order_id": oid, "discount_type": "coupon", "discount_amount": "1.00"},
    )
    assert od.status_code == 200
    assert (await client.get("/admin/order-discounts")).json()["data"]["total"] == 1

    ua = await client.post(
        "/admin/user-auths",
        json={"user_id": uid, "platform": "wechat", "openid": "o1"},
    )
    assert ua.status_code == 200
    assert (await client.get("/admin/user-auths")).json()["data"]["total"] == 1


@pytest.mark.asyncio
async def test_room_order_conflict_returns_409(client):
    on = f"O{uuid.uuid4().hex}"
    body = {"order_number": on}
    assert (await client.post("/admin/room-orders", json=body)).status_code == 200
    r2 = await client.post("/admin/room-orders", json=body)
    assert r2.status_code == 409
