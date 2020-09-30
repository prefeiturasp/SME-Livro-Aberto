from ..models import EscolaInfo, Dre

# pega todas as escolas
es = EscolaInfo.objects.all()
# cria atualiza PJ pra PJ Zona Norte
Dre.objects.filter(code="PJ").update(code="PJ ZN", name="DRE PIRITUBA/JARAGUA ZONA NORTE")
# cria DRE PJ Zona Oeste
try:
    dre_pj_zo = Dre.objects.get(code="PJ ZO")
except Dre.DoesNotExist:
    dre_pj_zo = Dre(name="DRE PIRITUBA/JARAGUA ZONA OESTE",
                    code="PJ ZO")
    dre_pj_zo.save()
# pega escolas que estão em PJ Zona Norte mas são Zona Oeste
escolas_dre_pj_zo = es.filter(dre__code="PJ ZN", distrito__zona="ZONA OESTE")
# atualiza a DRE dessas escolas
escolas_dre_pj_zo.update(dre=dre_pj_zo)

# cria atualiza IP para IP Centro
Dre.objects.filter(code="IP").update(code="IP CE", name="DRE IPIRANGA CENTRO")
# cria DREs IP Zona Leste e IP Zona Sul
try:
    dre_ip_zs = Dre.objects.get(code="IP ZS")
except Dre.DoesNotExist:
    dre_ip_zs = Dre(name="DRE IPIRANGA ZONA SUL",
                    code="IP ZS")
    dre_ip_zs.save()
try:
    dre_ip_zl = Dre.objects.get(code="IP ZL")
except Dre.DoesNotExist:
    dre_ip_zl = Dre(name="DRE IPIRANGA ZONA LESTE",
                    code="IP ZL")
    dre_ip_zl.save()

# pega escolas que estão em IP Centro mas são Zona Leste
escolas_dre_ip_zl = es.filter(dre__code="IP CE", distrito__zona="ZONA LESTE")
# atualiza a DRE dessas escolas
escolas_dre_ip_zl.update(dre=dre_ip_zl)

# pega escolas que estão em IP Centro mas são Zona Leste
escolas_dre_ip_zs = es.filter(dre__code="IP CE", distrito__zona="ZONA SUL")
# atualiza a DRE dessas escolas
escolas_dre_ip_zs.update(dre=dre_ip_zs)
