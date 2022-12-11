import xlrd
from Cadastro.models import Categoria, Produtos


def import_xlsx(filename):
    '''
    Importa planilhas xlsx.
    '''
    workbook = xlrd.open_workbook(filename)
    sheet = workbook.sheet_by_index(0)

    fields = ('nome', 'est_inic', 'est_min',
              'descricao', 'unid_medida', 'cod_produto', 'categoria_f_m')

    categorias = []
    for row in range(1, sheet.nrows):
        categoria = sheet.row(row)[6].value
        categorias.append(categoria)

    categorias_unicas = [Categoria(categoria=categoria)
                         for categoria in set(categorias) if categoria]

    # Categoria.fields.all().delete()  # CUIDADO
    Categoria.objects.bulk_create(categorias_unicas)

    aux = []
    for row in range(1, sheet.nrows):
        nome = sheet.row(row)[0].value
        est_inic = int(sheet.row(row)[1].value)

        est_min = int(sheet.row(row)[2].value)

        descricao = sheet.row(row)[3].value
        unid_medida = sheet.row(row)[4].value
        cod_produto = sheet.row(row)[5].value

        _categoria = sheet.row(row)[6].value
        categoria = Categoria.objects.filter(categoria=_categoria).first()

        produto = dict(
            nome=nome,
            est_inic=est_inic,
            est_min=est_min,
            descricao=descricao,
            unid_medida=unid_medida,
            cod_produto=cod_produto,
        )

        if categoria:
            obj = Produtos(categoria=categoria, **produto)
        else:
            obj = Produtos(**produto)

        aux.append(obj)

    Produtos.objects.all().delete()  # CUIDADO
    Produtos.objects.bulk_create(aux)
