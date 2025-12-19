class PetAPIRoutes:
    ADD_OR_UPDATE_PET = '/pet'
    DELETES_A_PET = '/pet/{pet_id}'
    GET_A_LIST_OF_PETS_BY_STATUS = '/pet/findByStatus'
    GET_A_LIST_OF_PETS_BY_TAGS = '/pet/findByTags'
    GET_PET_BY_ID = '/pet/{pet_id}'
    UPDATES_PET_IN_THE_STORE_WITH_FORM_DATA = '/pet/{pet_id}'
    UPLOADS_AN_IMAGE = '/pet/{pet_id}/uploadImage'
