"""Small, dependency-free message catalog. Scientific identifiers stay unchanged."""
from .translations import EXTRA_CATALOG

LANGUAGES = {"es": "Español", "en": "English", "pt": "Português",
             "de": "Deutsch", "fr": "Français", "zh": "简体中文", "ja": "日本語"}

# Spanish source text: (English, Portuguese). Keep named placeholders identical.
CATALOG = {
    "Idioma": ("Language", "Idioma"),
    "Interacciones proteína–ligando · análisis local": ("Protein–ligand interactions · local analysis", "Interações proteína–ligante · análise local"),
    "Análisis": ("Analysis", "Análise"),
    "Actualizar": ("Refresh", "Atualizar"),
    "Complejo": ("Complex", "Complexo"),
    "Python del entorno PLIP": ("Python in the PLIP environment", "Python do ambiente PLIP"),
    "Elegir…": ("Browse…", "Escolher…"),
    "Motor PLIP": ("PLIP engine", "Motor PLIP"),
    "Carpeta…": ("Folder…", "Pasta…"),
    "Resultados": ("Results", "Resultados"),
    "Añadir hidrógenos polares con PLIP": ("Add polar hydrogens with PLIP", "Adicionar hidrogênios polares com PLIP"),
    "Analizar complejo": ("Analyze complex", "Analisar complexo"),
    "Cancelar": ("Cancel", "Cancelar"),
    "Importar XML + PDB…": ("Import XML + PDB…", "Importar XML + PDB…"),
    "Selecciona un complejo que contenga proteína y ligando.": ("Select a complex containing a protein and a ligand.", "Selecione um complexo que contenha proteína e ligante."),
    "Ejemplo": ("Example", "Exemplo"),
    "Cargar ejemplo": ("Load example", "Carregar exemplo"),
    "Resultados precalculados; no requieren instalar PLIP.": ("Precomputed results; no PLIP installation required.", "Resultados pré-calculados; não é necessário instalar o PLIP."),
    "Mostrar interacciones": ("Show interactions", "Mostrar interações"),
    "Contacto hidrofóbico": ("Hydrophobic contact", "Contato hidrofóbico"),
    "Puente de hidrógeno": ("Hydrogen bond", "Ligação de hidrogênio"),
    "Puente de agua": ("Water bridge", "Ponte de água"),
    "Puente salino": ("Salt bridge", "Ponte salina"),
    "Apilamiento π–π": ("π–π stacking", "Empilhamento π–π"),
    "Interacción catión–π": ("Cation–π interaction", "Interação cátion–π"),
    "Enlace de halógeno": ("Halogen bond", "Ligação de halogênio"),
    "Coordinación metálica": ("Metal coordination", "Coordenação metálica"),
    "Color…": ("Color…", "Cor…"),
    "Radio de línea (Å)": ("Line radius (Å)", "Raio da linha (Å)"),
    "Distancias 3D": ("3D distances", "Distâncias 3D"),
    "Aplicar estilo": ("Apply style", "Aplicar estilo"),
    "Interacción": ("Interaction", "Interação"),
    "Residuo": ("Residue", "Resíduo"),
    "Distancia (Å)": ("Distance (Å)", "Distância (Å)"),
    "Ángulos (°)": ("Angles (°)", "Ângulos (°)"),
    "Centros {distance}": ("Centers {distance}", "Centros {distance}"),
    "Pulsa una fila para centrar y etiquetar sus residuos.\nLas líneas representan el análisis guardado; no son un cálculo dinámico.": ("Click a row to focus and label its residues.\nLines show the saved analysis; they are not a live calculation.", "Clique em uma linha para centralizar e rotular seus resíduos.\nAs linhas representam a análise salva; não são um cálculo dinâmico."),
    "Exportar CSV…": ("Export CSV…", "Exportar CSV…"),
    "Guardar sesión…": ("Save session…", "Salvar sessão…"),
    "Ver bitácora": ("Show log", "Ver registro"),
    "Seleccionar Python del entorno PLIP": ("Select Python in the PLIP environment", "Selecionar Python do ambiente PLIP"),
    "Carpeta de resultados": ("Results folder", "Pasta de resultados"),
    "Abre y selecciona un complejo molecular.": ("Open and select a molecular complex.", "Abra e selecione um complexo molecular."),
    "Esta versión necesita cadenas de un carácter y numeración compatible con PDB.": ("This version requires single-character chains and PDB-compatible numbering.", "Esta versão requer cadeias de um caractere e numeração compatível com PDB."),
    "Selecciona un complejo de menos de 100 000 átomos.": ("Select a complex with fewer than 100,000 atoms.", "Selecione um complexo com menos de 100.000 átomos."),
    "Configura la ruta al Python del entorno PLIP (consulta la guía).": ("Set the path to Python in the PLIP environment (see the guide).", "Configure o caminho do Python do ambiente PLIP (consulte o guia)."),
    "PLIP está analizando el complejo… Puedes seguir usando ChimeraX.": ("PLIP is analyzing the complex… You can keep using ChimeraX.", "O PLIP está analisando o complexo… Você pode continuar usando o ChimeraX."),
    "Cancelando PLIP…": ("Canceling PLIP…", "Cancelando o PLIP…"),
    "Análisis cancelado. La bitácora se conserva.": ("Analysis canceled. The log is preserved.", "Análise cancelada. O registro foi preservado."),
    "Informe PLIP": ("PLIP report", "Relatório PLIP"),
    "PDB original/corregido utilizado por PLIP": ("Original/corrected PDB used by PLIP", "PDB original/corrigido utilizado pelo PLIP"),
    "Se requiere un único modelo en el PDB analizado.": ("The analyzed PDB must contain a single model.", "O PDB analisado deve conter um único modelo."),
    "estructura analizada": ("analyzed structure", "estrutura analisada"),
    "PLIP no detectó ligandos analizables. Consulta plip.log.": ("PLIP found no analyzable ligands. See plip.log.", "O PLIP não detectou ligantes analisáveis. Consulte plip.log."),
    "{site} · {count} interacciones": ("{site} · {count} interactions", "{site} · {count} interações"),
    "La geometría cambió o el modelo se cerró. Ejecuta un nuevo análisis.": ("The geometry changed or the model was closed. Run a new analysis.", "A geometria mudou ou o modelo foi fechado. Execute uma nova análise."),
    " · {count} advertencias (Log)": (" · {count} warnings (Log)", " · {count} avisos (Log)"),
    "PLIP {version} · {count} interacciones{warnings}": ("PLIP {version} · {count} interactions{warnings}", "PLIP {version} · {count} interações{warnings}"),
    "Geometría o numeración modificada: interacciones ocultas. Vuelve a analizar.": ("Geometry or numbering changed: interactions hidden. Run the analysis again.", "Geometria ou numeração modificada: interações ocultas. Execute a análise novamente."),
    "Recalcula el análisis antes de exportar una estructura modificada.": ("Run the analysis again before exporting a modified structure.", "Execute a análise novamente antes de exportar uma estrutura modificada."),
    "Exportar interacciones": ("Export interactions", "Exportar interações"),
    "Guardar sesión ChimeraX": ("Save ChimeraX session", "Salvar sessão do ChimeraX"),
    "Todavía no hay una ejecución.": ("No run is available yet.", "Ainda não há uma execução."),
    "Resultados PLIP: {path}": ("PLIP results: {path}", "Resultados PLIP: {path}"),
    "Ejemplo precalculado {name}: no se ejecutó el motor PLIP.": ("Precomputed example {name}: the PLIP engine was not run.", "Exemplo pré-calculado {name}: o motor PLIP não foi executado."),
    "Versión de sesión PLIP Explorer no compatible.": ("Unsupported PLIP Explorer session version.", "Versão de sessão do PLIP Explorer não compatível."),
    "Sesión PLIP restaurada.": ("PLIP session restored.", "Sessão PLIP restaurada."),
    "Análisis desactualizado; vuelve a analizar.": ("Outdated analysis; run the analysis again.", "Análise desatualizada; execute a análise novamente."),
    "interacciones PLIP": ("PLIP interactions", "interações PLIP"),
    "Coordenada no finita": ("Non-finite coordinate", "Coordenada não finita"),
    "El XML supera el límite de 30 MB de esta versión.": ("The XML exceeds this version's 30 MB limit.", "O XML excede o limite de 30 MB desta versão."),
    "El informe no debe contener DTD ni entidades XML.": ("The report must not contain a DTD or XML entities.", "O relatório não deve conter DTD nem entidades XML."),
    "No es un informe XML de PLIP (falta <report>).": ("Not a PLIP XML report (missing <report>).", "Não é um relatório XML do PLIP (falta <report>)."),
    "Sitio {index}: faltan identificadores del ligando.": ("Site {index}: missing ligand identifiers.", "Sítio {index}: faltam identificadores do ligante."),
    "{key}: falta el bloque interactions.": ("{key}: missing interactions block.", "{key}: falta o bloco interactions."),
    "Categoría no implementada: {kind}.": ("Unsupported category: {kind}.", "Categoria não implementada: {kind}."),
    "Falta {field}": ("Missing {field}", "Falta {field}"),
    "Interacción {uid} omitida: {error}": ("Interaction {uid} omitted: {error}", "Interação {uid} omitida: {error}"),
    "desconocida": ("unknown", "desconhecida"),
    "La entrada no contiene átomos PDB.": ("The input contains no PDB atoms.", "A entrada não contém átomos PDB."),
    "Exporta un único modelo/conformación antes de analizar.": ("Export a single model/conformation before analysis.", "Exporte um único modelo/conformação antes de analisar."),
    "Esta versión requiere un complejo de menos de 100 000 átomos.": ("This version requires a complex with fewer than 100,000 atoms.", "Esta versão requer um complexo com menos de 100.000 átomos."),
    "Registro PDB incompleto.": ("Incomplete PDB record.", "Registro PDB incompleto."),
    "Resuelve las conformaciones alternativas y exporta una sola antes de analizar.": ("Resolve alternate conformations and export only one before analysis.", "Resolva as conformações alternativas e exporte apenas uma antes de analisar."),
    "Esta versión requiere residuos sin códigos de inserción. Usa una copia renumerada.": ("This version requires residues without insertion codes. Use a renumbered copy.", "Esta versão requer resíduos sem códigos de inserção. Use uma cópia renumerada."),
    "Numeración o coordenadas incompatibles con PDB estándar.": ("Numbering or coordinates incompatible with standard PDB.", "Numeração ou coordenadas incompatíveis com PDB padrão."),
    "Falta un ligando en registros HETATM. El complejo debe incluir proteína y ligando.": ("No ligand in HETATM records. The complex must include a protein and a ligand.", "Falta um ligante nos registros HETATM. O complexo deve incluir proteína e ligante."),
    "El PDB no coincide con {count} interacción(es) del XML. Selecciona la estructura analizada por PLIP.": ("The PDB does not match {count} interaction(s) in the XML. Select the structure analyzed by PLIP.", "O PDB não corresponde a {count} interação(ões) do XML. Selecione a estrutura analisada pelo PLIP."),
    "El informe de grupos requiere IDs atómicos únicos y el PDB original/corregido de PLIP.": ("Group interactions require unique atom IDs and PLIP's original/corrected PDB.", "As interações de grupos requerem IDs atômicos únicos e o PDB original/corrigido do PLIP."),
    "No coincide el centro geométrico de {uid}. Usa el PDB original/corregido del informe.": ("The geometric center of {uid} does not match. Use the report's original/corrected PDB.", "O centro geométrico de {uid} não corresponde. Use o PDB original/corrigido do relatório."),
    "Selecciona el ejecutable Python del entorno que contiene PLIP.": ("Select the Python executable in the environment containing PLIP.", "Selecione o executável Python do ambiente que contém o PLIP."),
    "La carpeta ya contiene un informe; usa una carpeta de ejecución nueva.": ("The folder already contains a report; use a new run folder.", "A pasta já contém um relatório; use uma nova pasta de execução."),
    "Análisis cancelado.": ("Analysis canceled.", "Análise cancelada."),
    "PLIP superó {seconds} segundos.": ("PLIP exceeded {seconds} seconds.", "O PLIP excedeu {seconds} segundos."),
    "PLIP terminó con código {code}. Revisa {path}": ("PLIP exited with code {code}. Check {path}", "O PLIP terminou com código {code}. Consulte {path}"),
    "PLIP no produjo report.xml. Revisa plip.log.": ("PLIP did not produce report.xml. Check plip.log.", "O PLIP não produziu report.xml. Consulte plip.log."),
    "No se encontró la estructura exacta indicada por PLIP.": ("The exact structure specified by PLIP was not found.", "A estrutura exata indicada pelo PLIP não foi encontrada."),
}

# Resolve by language code, independently of the selector order.
CATALOG = {source: dict(zip(("en", "pt"), texts)) for source, texts in CATALOG.items()}
for _source, _texts in EXTRA_CATALOG.items():
    CATALOG.setdefault(_source, {}).update(zip(("de", "fr", "zh", "ja"), _texts))


class Message(str):
    """Preserve a template through exceptions; remain JSON/CSV compatible."""
    def __new__(cls, source, **values):
        obj = super().__new__(cls, source.format(**values))
        obj.source, obj.values = source, values
        return obj


def message(source, **values):
    return Message(source, **values)


def translate(source, language="es", **values):
    if isinstance(source, BaseException):
        source = source.args[0] if len(source.args) == 1 else str(source)
    if isinstance(source, Message):
        values = {**source.values, **values}
        source = source.source
    source = str(source)
    text = CATALOG.get(source, {}).get(language, source)
    values = {k: translate(v, language) if isinstance(v, (Message, BaseException)) else v
              for k, v in values.items()}
    return text.format(**values) if values else text
