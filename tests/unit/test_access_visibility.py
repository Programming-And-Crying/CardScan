from access.selectors import visible_contacts_for_user


def test_admin_sees_everything(admin_user, visible_contact):
    qs = visible_contacts_for_user(admin_user)
    assert visible_contact in qs


def test_office_user_sees_intersection_only(office_user, sales_group, visible_contact):
    office_user.access_groups.add(sales_group)
    qs = visible_contacts_for_user(office_user)
    assert visible_contact in qs
