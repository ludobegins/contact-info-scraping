import empresas_aux
import contact_info

bad_words = ['twitter','facebook','instagram']
for i in [0,1]:
        empresa = empresas_aux.lista_empresas[i]
        df = contact_info.get_info([empresa,"sustentabilidade"], 5, 'pt-BR', f'{empresa}.csv', reject=bad_words)
        print(df.head(10))