from django.db.models import Q


def qr_and_or(campo, pesq):
    var = pesq.split(' && ')
    q = Q()
    for v_and in var:
        v_or = ''
        v_or = v_and.split(' || ')
        if len(v_or)>1:
            for v in v_or:
                q |= Q(**{campo: v})
        else:
            q &= Q(**{campo: v_and})
    return q
