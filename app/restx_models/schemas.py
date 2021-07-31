
from flask_restx import fields, Namespace

api = Namespace("Translation Models", description = "namespace for language translation API models")

#-----------------------------#
# Language Translation Single #
#-----------------------------#
translation_single_schema = {
    "text": fields.String(description = "Text to be translated by API", required = True),
    "from_lang": fields.String(description = "2-3 letter abbreviation of language to translate from", required = True),
    "to_lang": fields.String(description = "2-3 letter abbreviation of language to translated to", required = True)
}
translation_single_model = api.model("translation_single", translation_single_schema)

#----------------------------#
# Language Translation Batch #
#----------------------------#
translation_batch_schema = {
    "text": fields.List(fields.Nested(api.model("translation_single")), required = True)
}
translation_batch_model = api.model("translation_batch", translation_batch_schema)