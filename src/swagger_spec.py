SWAGGER_SPEC = {
    "swagger": "2.0",
    "info": {
        "title": "Gestion de Huellas de Calzado",
        "description": "API documentada para el Trabajo Practico Integrador de Laboratorio de Lenguajes",
        "version": "1.0.0"
    },
    "host": "localhost:5000",
    "schemes": [
        "http"
    ],
    "consumes": [
        "application/json"
    ],
    "produces": [
        "application/json"
    ],
    "securityDefinitions": {
        "JWT": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": 'Ingresa el token JWT con el prefijo "Bearer " (ej. "Bearer eyJhbGciOiJIUzI1NiIsIHNvbWV0b2tlbi")'
        }
    },
    "definitions": {
        "Calzado": {
            "type": "object",
            "properties": {
                "id_calzado": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del calzado"},
                "talle": {"type": "string", "maxLength": 10, "nullable": True, "description": "Talle del calzado"},
                "ancho": {"type": "number", "format": "float", "nullable": True, "description": "Ancho del calzado"},
                "alto": {"type": "number", "format": "float", "nullable": True, "description": "Alto del calzado"},
                "tipo_registro": {
                    "type": "string",
                    "enum": ["indubitada_proveedor", "indubitada_comisaria", "dubitada"],
                    "nullable": True,
                    "description": "Tipo de registro del calzado"
                },
                "id_marca": {"type": "integer", "format": "int32", "nullable": True, "description": "ID de la marca (clave foránea)"},
                "marca": {"type": "string", "nullable": True, "description": "Nombre de la marca (para respuestas GET)"},
                "id_modelo": {"type": "integer", "format": "int32", "nullable": True, "description": "ID del modelo (clave foránea)"},
                "modelo": {"type": "string", "nullable": True, "description": "Nombre del modelo (para respuestas GET)"},
                "id_categoria": {"type": "integer", "format": "int32", "nullable": True, "description": "ID de la categoría (clave foránea)"},
                "categoria": {"type": "string", "nullable": True, "description": "Nombre de la categoría (para respuestas GET)"},
                "colores": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Lista de nombres de colores asociados al calzado (para respuestas GET)"
                }
            },
            "required": [
                "talle",
                "ancho",
                "alto",
                "id_categoria",
                "id_marca",
                "id_modelo"
            ]
        },
        "CalzadoInput": {
            "type": "object",
            "properties": {
                "talle": {"type": "string", "maxLength": 10, "nullable": True, "description": "Talle del calzado"},
                "ancho": {"type": "number", "format": "float", "nullable": True, "description": "Ancho del calzado"},
                "alto": {"type": "number", "format": "float", "nullable": True, "description": "Alto del calzado"},
                "tipo_registro": {
                    "type": "string",
                    "enum": ["indubitada_proveedor", "indubitada_comisaria", "dubitada"],
                    "nullable": True,
                    "description": "Tipo de registro del calzado"
                },
                "id_marca": {"type": "integer", "format": "int32", "nullable": True, "description": "ID de la marca"},
                "id_modelo": {"type": "integer", "format": "int32", "nullable": True, "description": "ID del modelo"},
                "id_categoria": {"type": "integer", "format": "int32", "nullable": True, "description": "ID de la categoría"},
                "id_colores": {
                    "type": "array",
                    "items": {"type": "integer", "format": "int32"},
                    "description": "Lista de IDs de colores para asociar"
                }
            },
            "required": [
                "talle",
                "ancho",
                "alto",
                "id_marca",
                "id_modelo",
                "id_categoria",
                "id_colores"
            ]
        },
        "CalzadoImputadoInput": {
            "type": "object",
            "properties": {
                "id_calzado": {"type": "integer", "format": "int32", "description": "ID del calzado"},
                "id_imputado": {"type": "integer", "format": "int32", "description": "ID del imputado"}
            },
            "required": [
                "id_calzado",
                "id_imputado"
            ]
        },
        "Suela": {
            "type": "object",
            "properties": {
                "id_suela": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único de la suela"},
                "id_calzado": {"type": "integer", "format": "int32", "description": "ID del calzado al que pertenece la suela"},
                "descripcion_general": {"type": "string", "nullable": True, "description": "Descripción general de la suela"},
                "detalles": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/DetalleSuelaOutput"},
                    "description": "Lista de detalles de la suela (para respuestas GET)"
                }
            },
            "required": ["id_calzado"]
        },
        "SuelaInput": {
            "type": "object",
            "properties": {
                "id_calzado": {"type": "integer", "format": "int32", "description": "ID del calzado al que pertenece la suela"},
                "descripcion_general": {"type": "string", "nullable": True, "description": "Descripción general de la suela"},
                "detalles": {
                    "type": "array",
                    "items": {"$ref": "#/definitions/DetalleSuelaInput"},
                    "description": "Lista de detalles de la suela"
                }
            },
            "required": ["id_calzado"]
        },
        "DetalleSuelaOutput": {
            "type": "object",
            "properties": {
                "id_detalle": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del detalle de suela"},
                "id_cuadrante": {"type": "integer", "format": "int32", "description": "ID del cuadrante"},
                "cuadrante_nombre": {"type": "string", "description": "Nombre del cuadrante (si se carga en to_dict)"},
                "id_forma": {"type": "integer", "format": "int32", "description": "ID de la forma geométrica"},
                "forma_nombre": {"type": "string", "description": "Nombre de la forma geométrica (si se carga en to_dict)"},
                "detalle_adicional": {"type": "string", "nullable": True, "description": "Detalle adicional del área"}
            },
            "required": ["id_cuadrante", "id_forma"]
        },
        "DetalleSuelaInput": {
            "type": "object",
            "properties": {
                "id_cuadrante": {"type": "integer", "format": "int32", "description": "ID del cuadrante"},
                "id_forma": {"type": "integer", "format": "int32", "description": "ID de la forma geométrica"},
                "detalle_adicional": {"type": "string", "nullable": True, "description": "Detalle adicional del área"}
            },
            "required": ["id_cuadrante", "id_forma"]
        },
        "FormaGeometrica": {
            "type": "object",
            "properties": {
                "id_forma": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único de la forma geométrica"},
                "nombre": {"type": "string", "maxLength": 50, "description": "Nombre de la forma geométrica"}
            },
            "required": ["nombre"]
        },
        "Cuadrante": {
            "type": "object",
            "properties": {
                "id_cuadrante": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del cuadrante"},
                "nombre": {"type": "string", "maxLength": 50, "description": "Nombre del cuadrante"}
            },
            "required": ["nombre"]
        },
        "Usuario": {
            "type": "object",
            "properties": {
                "id": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del usuario"},
                "username": {"type": "string", "maxLength": 50, "description": "Nombre de usuario"},
                "role": {"type": "string", "maxLength": 20, "description": "Rol del usuario (ej. 'admin', 'user')"}
            },
            "required": ["username", "role"]
        },
        "UsuarioInput": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "maxLength": 50, "description": "Nombre de usuario"},
                "password": {"type": "string", "description": "Contraseña (solo para creación y actualización)"},
                "role": {"type": "string", "maxLength": 20, "description": "Rol del usuario (ej. 'admin', 'user')"}
            },
            "required": ["username", "password", "role"]
        },
        "LoginInput": {
            "type": "object",
            "properties": {
                "username": {"type": "string", "description": "Nombre de usuario"},
                "password": {"type": "string", "description": "Contraseña"}
            },
            "required": ["username", "password"]
        },
        "LoginResponse": {
            "type": "object",
            "properties": {
                "success": {"type": "boolean", "description": "Indica si el inicio de sesión fue exitoso"},
                "message": {"type": "string", "description": "Mensaje de resultado"},
                "token": {"type": "string", "description": "Token JWT para autenticación"},
                "user": {
                    "type": "object",
                    "properties": {
                        "id": {"type": "integer", "format": "int32"},
                        "username": {"type": "string"},
                        "role": {"type": "string"}
                    }
                }
            }
        },
        "Marca": {
            "type": "object",
            "properties": {
                "id_marca": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único de la marca"},
                "nombre": {"type": "string", "maxLength": 50, "description": "Nombre de la marca"}
            },
            "required": ["nombre"]
        },
        "Categoria": {
            "type": "object",
            "properties": {
                "id_categoria": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único de la categoría"},
                "nombre": {"type": "string", "maxLength": 50, "description": "Nombre de la categoría"}
            },
            "required": ["nombre"]
        },
        "Color": {
            "type": "object",
            "properties": {
                "id_color": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del color"},
                "nombre": {"type": "string", "maxLength": 50, "description": "Nombre del color"}
            },
            "required": ["nombre"]
        },
        "Modelo": {
            "type": "object",
            "properties": {
                "id_modelo": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del modelo"},
                "nombre": {"type": "string", "maxLength": 100, "description": "Nombre del modelo"}
            },
            "required": ["nombre"]
        },
        "Imputado": {
            "type": "object",
            "properties": {
                "id_imputado": {"type": "integer", "format": "int32", "readOnly": True, "description": "ID único del imputado"},
                "nombre": {"type": "string", "maxLength": 100, "description": "Nombre del imputado"},
                "apellido": {"type": "string", "maxLength": 100, "description": "Apellido del imputado"},
                "dni": {"type": "string", "maxLength": 20, "description": "DNI del imputado"},
                "direccion": {"type": "string", "maxLength": 255, "description": "Dirección del imputado"},
                "comisaria": {"type": "string", "maxLength": 255, "description": "Comisaría de referencia del imputado"},
                "jurisdiccion": {"type": "string", "maxLength": 255, "description": "Jurisdicción del imputado"},
                "calzados": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id_calzado": {"type": "integer", "format": "int32"},
                            "talle": {"type": "string"},
                            "ancho": {"type": "number", "format": "float"},
                            "alto": {"type": "number", "format": "float"},
                            "tipo_registro": {"type": "string"},
                            "marca": {"type": "string"},
                            "modelo": {"type": "string"},
                            "categoria": {"type": "string"},
                            "colores": {
                                "type": "array",
                                "items": {"type": "string"}
                            }
                        }
                    },
                    "description": "Lista de calzados asociados al imputado"
                }
            },
            "required": ["nombre", "apellido", "dni", "direccion", "comisaria", "jurisdiccion"]
        },
        "MessageResponse": {
            "type": "object",
            "properties": {
                "message": {"type": "string"}
            }
        },
        "ErrorResponse": {
            "type": "object",
            "properties": {
                "error": {"type": "string"}
            }
        }
    },
    "paths": {
        "/auth/login": {
            "post": {
                "tags": ["Autenticación"],
                "summary": "Iniciar sesión y obtener un token JWT.",
                "parameters": [
                    {
                        "in": "body",
                        "name": "credentials",
                        "description": "Credenciales de usuario para el inicio de sesión.",
                        "required": True,
                        "schema": {"$ref": "#/definitions/LoginInput"}
                    }
                ],
                "responses": {
                    "200": {"description": "Inicio de sesión exitoso.", "schema": {"$ref": "#/definitions/LoginResponse"}},
                    "400": {"description": "Usuario o contraseña obligatorios.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "401": {"description": "Credenciales incorrectas.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "options": {
                "tags": ["Autenticación"],
                "summary": "Manejar solicitudes OPTIONS para el preflight de CORS.",
                "responses": {
                    "200": {"description": "Respuesta exitosa para la solicitud OPTIONS."}
                }
            }
        },
        "/usuarios": {
            "post": {
                "tags": ["Usuarios"],
                "summary": "Crear un nuevo usuario.",
                "description": "Este endpoint permite crear un nuevo usuario con nombre de usuario, contraseña y rol.",
                "parameters": [
                    {
                        "in": "body",
                        "name": "user",
                        "description": "Objeto de usuario a crear.",
                        "required": True,
                        "schema": {"$ref": "#/definitions/UsuarioInput"}
                    }
                ],
                "responses": {
                    "201": {"description": "Usuario creado exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "Datos de entrada inválidos (campos obligatorios faltantes, rol no válido, contraseña corta o usuario existente).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "get": {
                "tags": ["Usuarios"],
                "summary": "Obtener todos los usuarios registrados.",
                "security": [{"JWT": []}],
                "responses": {
                    "200": {"description": "Lista de usuarios.", "schema": {"type": "array", "items": {"$ref": "#/definitions/Usuario"}}},
                    "404": {"description": "No hay usuarios registrados.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/me": {
            "get": {
                "tags": ["Usuarios"],
                "summary": "Obtener información del usuario autenticado.",
                "description": "Este endpoint devuelve los detalles del usuario cuya sesión está activa, basándose en el token JWT proporcionado.",
                "security": [{"JWT": []}],
                "responses": {
                    "200": {"description": "Información del usuario actual.", "schema": {"$ref": "#/definitions/Usuario"}},
                    "401": {"description": "No autorizado (token faltante o inválido).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Usuario no encontrado (raro si el token es válido).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/usuarios/{user_id}": {
            "patch": {
                "tags": ["Usuarios"],
                "summary": "Actualizar un usuario por su ID.",
                "description": "Permite a un usuario actualizar su propio perfil o a un administrador actualizar cualquier usuario.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "user_id",
                        "type": "integer",
                        "required": True,
                        "description": "ID del usuario a actualizar."
                    },
                    {
                        "in": "body",
                        "name": "user_data",
                        "description": "Campos a actualizar del usuario (username, password, role).",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "username": {"type": "string", "maxLength": 50},
                                "password": {"type": "string"},
                                "role": {"type": "string", "maxLength": 20, "enum": ["admin", "user", "moderator"]}
                            },
                            "minProperties": 1
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Usuario actualizado exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "new_token": {"type": "string", "description": "Nuevo token JWT si se actualiza el perfil del usuario autenticado."}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (contraseña corta, nombre de usuario duplicado, no se dieron datos para actualizar, rol no válido).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "403": {"description": "No tienes permisos para actualizar este usuario o cambiar roles.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Usuario no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/usuarios/{id}": {
            "get": {
                "tags": ["Usuarios"],
                "summary": "Obtener un usuario por su ID.",
                "description": "Este endpoint devuelve los detalles de un usuario específico utilizando su ID.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "type": "integer",
                        "required": True,
                        "description": "ID único del usuario a obtener."
                    }
                ],
                "responses": {
                    "200": {"description": "Detalles del usuario.", "schema": {"$ref": "#/definitions/Usuario"}},
                    "401": {"description": "No autorizado (token faltante o inválido).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Usuario no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "delete": {
                "tags": ["Usuarios"],
                "summary": "Eliminar un usuario por su ID.",
                "description": "Este endpoint permite eliminar un usuario específico.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "type": "integer",
                        "required": True,
                        "description": "ID del usuario a eliminar."
                    }
                ],
                "responses": {
                    "200": {"description": "Usuario eliminado exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "401": {"description": "No autorizado (token faltante o inválido).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Usuario no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/calzados": {
            "get": {
                "tags": ["Calzados"],
                "summary": "Obtener todos los calzados registrados.",
                "security": [{"JWT": []}],
                "responses": {
                    "200": {"description": "Lista de calzados.", "schema": {"type": "array", "items": {"$ref": "#/definitions/Calzado"}}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "post": {
                "tags": ["Calzados"],
                "summary": "Crear un nuevo calzado.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "body",
                        "name": "calzado",
                        "description": "Objeto de calzado a crear.",
                        "required": True,
                        "schema": {"$ref": "#/definitions/CalzadoInput"}
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Calzado creado exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "calzado": {"$ref": "#/definitions/Calzado"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación o ID(s) de entidad relacionada no válido(s).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/calzados/{id}": {
            "get": {
                "tags": ["Calzados"],
                "summary": "Obtener un calzado por su ID.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "type": "integer",
                        "required": True,
                        "description": "ID único del calzado a obtener."
                    }
                ],
                "responses": {
                    "200": {"description": "Detalles del calzado.", "schema": {"$ref": "#/definitions/Calzado"}},
                    "404": {"description": "Calzado no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "patch": {
                "tags": ["Calzados"],
                "summary": "Actualizar parcialmente un calzado existente.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "type": "integer",
                        "required": True,
                        "description": "ID del calzado a actualizar."
                    },
                    {
                        "in": "body",
                        "name": "calzado",
                        "description": "Objeto de calzado con los campos a actualizar.",
                        "required": True,
                        "schema": {"$ref": "#/definitions/CalzadoInput"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Calzado actualizado exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "calzado": {"$ref": "#/definitions/Calzado"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación o ID(s) de entidad relacionada no válido(s).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Calzado no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "delete": {
                "tags": ["Calzados"],
                "summary": "Eliminar un calzado por su ID.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "type": "integer",
                        "required": True,
                        "description": "ID del calzado a eliminar."
                    }
                ],
                "responses": {
                    "200": {"description": "Calzado eliminado exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "El calzado no puede ser eliminado porque tiene suelas o imputados asociados.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Calzado no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/calzados/{id}/imputados": {
            "post": {
                "tags": ["Calzados", "Imputados"],
                "summary": "Asocia un calzado a uno o más imputados.",
                "description": "Este endpoint permite vincular un calzado existente con uno o más imputados existentes.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "type": "integer",
                        "required": True,
                        "description": "ID del calzado al que se asociarán los imputados."
                    },
                    {
                        "in": "body",
                        "name": "imputados_data",
                        "description": "Lista de IDs de imputados a asociar.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "id_imputados": {
                                    "type": "array",
                                    "items": {"type": "integer", "format": "int32"},
                                    "description": "Lista de IDs de imputados."
                                }
                            },
                            "required": ["id_imputados"]
                        }
                    }
                ],
                "responses": {
                    "200": {"description": "Imputados asociados exitosamente al calzado.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "Datos de entrada inválidos (calzado no encontrado, imputado(s) no encontrado(s), imputado(s) ya asociado(s)).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Calzado no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/calzados/{id_calzado}/imputados/{id_imputado}": {
            "delete": {
                "tags": ["Calzados", "Imputados"],
                "summary": "Desasocia un calzado de un imputado.",
                "description": "Este endpoint permite desvincular un calzado de un imputado específico.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_calzado",
                        "type": "integer",
                        "required": True,
                        "description": "ID del calzado a desasociar."
                    },
                    {
                        "in": "path",
                        "name": "id_imputado",
                        "type": "integer",
                        "required": True,
                        "description": "ID del imputado a desasociar."
                    }
                ],
                "responses": {
                    "200": {"description": "Relación calzado-imputado eliminada exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "No se encontró la relación calzado-imputado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Calzado o imputado no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/suelas": {
            "post": {
                "tags": ["Suelas"],
                "summary": "Crear una nueva suela con sus detalles.",
                "description": "Este endpoint permite crear una nueva suela asociada a un calzado, incluyendo los detalles por cuadrante y forma.",
                "parameters": [
                    {
                        "in": "body",
                        "name": "suela",
                        "description": "Objeto de suela a crear, incluyendo sus detalles.",
                        "required": True,
                        "schema": {"$ref": "#/definitions/SuelaInput"}
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Suela creada exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "msg": {"type": "string"},
                                "suela": {"$ref": "#/definitions/Suela"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (ID de calzado, cuadrante o forma no válidos, o datos faltantes).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "get": {
                "tags": ["Suelas"],
                "summary": "Obtener todas las suelas registradas.",
                "description": "Este endpoint devuelve una lista de todas las suelas con sus detalles asociados.",
                "responses": {
                    "200": {"description": "Lista de suelas.", "schema": {"type": "array", "items": {"$ref": "#/definitions/Suela"}}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/suelas/{id}": {
            "get": {
                "tags": ["Suelas"],
                "summary": "Obtener una suela por su ID.",
                "description": "Este endpoint devuelve los detalles de una suela específica utilizando su ID.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id",
                        "type": "integer",
                        "required": True,
                        "description": "ID único de la suela a obtener."
                    }
                ],
                "responses": {
                    "200": {"description": "Detalles de la suela.", "schema": {"$ref": "#/definitions/Suela"}},
                    "400": {"description": "ID de suela inválido.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Suela no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/suelas/{id_suela}": {
            "put": {
                "tags": ["Suelas"],
                "summary": "Actualizar completamente una suela existente (reemplaza detalles).",
                "description": "Este endpoint permite actualizar los campos 'id_calzado' y 'descripcion_general' de una suela. Si se incluyen 'detalles', estos reemplazarán completamente los detalles existentes de la suela.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_suela",
                        "type": "integer",
                        "required": True,
                        "description": "ID de la suela a actualizar."
                    },
                    {
                        "in": "body",
                        "name": "suela",
                        "description": "Objeto de suela con los campos a actualizar. Los detalles si se envían, reemplazan los existentes.",
                        "required": True,
                        "schema": {"$ref": "#/definitions/SuelaInput"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Suela actualizada exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "suela": {"$ref": "#/definitions/Suela"}
                            }
                        }
                    },
                    "400": {"description": "No se recibieron datos JSON, o ID de calzado/cuadrante/forma no válido.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Suela no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "delete": {
                "tags": ["Suelas"],
                "summary": "Eliminar una suela por su ID.",
                "description": "Este endpoint permite eliminar una suela específica y todos sus detalles asociados.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_suela",
                        "type": "integer",
                        "required": True,
                        "description": "ID de la suela a eliminar."
                    }
                ],
                "responses": {
                    "200": {"description": "Suela eliminada exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "404": {"description": "Suela no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/suelas/{id_suela}/partial": {
            "patch": {
                "tags": ["Suelas"],
                "summary": "Actualizar parcialmente una suela existente.",
                "description": "Este endpoint permite modificar los campos 'id_calzado' y 'descripcion_general' de una suela. Si se incluyen 'detalles', estos reemplazarán completamente los detalles existentes de la suela.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_suela",
                        "type": "integer",
                        "required": True,
                        "description": "ID de la suela a actualizar parcialmente."
                    },
                    {
                        "in": "body",
                        "name": "suela",
                        "description": "Objeto de suela con los campos a actualizar. Si se envían detalles, reemplazan los existentes.",
                        "required": True,
                        "schema": {"$ref": "#/definitions/SuelaInput"}
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Suela actualizada parcialmente con éxito.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "suela": {"$ref": "#/definitions/Suela"}
                            }
                        }
                    },
                    "400": {"description": "No se recibieron datos JSON, o ID de calzado/cuadrante/forma no válido.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Suela no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/formas_geometricas": {
            "get": {
                "tags": ["Formas Geométricas"],
                "summary": "Obtener todas las formas geométricas registradas.",
                "responses": {
                    "200": {"description": "Lista de formas geométricas.", "schema": {"type": "array", "items": {"$ref": "#/definitions/FormaGeometrica"}}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "post": {
                "tags": ["Formas Geométricas"],
                "summary": "Crear una nueva forma geométrica.",
                "description": "Este endpoint permite crear una nueva forma geométrica con un nombre único.",
                "parameters": [
                    {
                        "in": "body",
                        "name": "forma",
                        "description": "Objeto de forma geométrica a crear.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nombre de la nueva forma geométrica."}
                            },
                            "required": ["nombre"]
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Forma geométrica creada exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "forma_geometrica": {"$ref": "#/definitions/FormaGeometrica"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (nombre requerido o duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/formas_geometricas/{id_forma}": {
            "get": {
                "tags": ["Formas Geométricas"],
                "summary": "Obtener una forma geométrica por su ID.",
                "description": "Este endpoint devuelve los detalles de una forma geométrica específica utilizando su ID.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_forma",
                        "type": "integer",
                        "required": True,
                        "description": "ID único de la forma geométrica a obtener."
                    }
                ],
                "responses": {
                    "200": {"description": "Detalles de la forma geométrica.", "schema": {"$ref": "#/definitions/FormaGeometrica"}},
                    "404": {"description": "Forma geométrica no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "patch": {
                "tags": ["Formas Geométricas"],
                "summary": "Actualizar el nombre de una forma geométrica existente.",
                "description": "Este endpoint permite modificar el nombre de una forma geométrica específica. El nuevo nombre debe ser único.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_forma",
                        "type": "integer",
                        "required": True,
                        "description": "ID de la forma geométrica a actualizar."
                    },
                    {
                        "in": "body",
                        "name": "forma",
                        "description": "Objeto con el nuevo nombre de la forma geométrica.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nuevo nombre para la forma geométrica."}
                            },
                            "required": ["nombre"]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Forma geométrica actualizada exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "forma_geometrica": {"$ref": "#/definitions/FormaGeometrica"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (nombre requerido o duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Forma geométrica no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "delete": {
                "tags": ["Formas Geométricas"],
                "summary": "Eliminar una forma geométrica por su ID.",
                "description": "Este endpoint permite eliminar una forma geométrica específica, siempre y cuando no esté siendo utilizada por ningún detalle de suela.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_forma",
                        "type": "integer",
                        "required": True,
                        "description": "ID de la forma geométrica a eliminar."
                    }
                ],
                "responses": {
                    "200": {"description": "Forma geométrica eliminada exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "No se puede eliminar la forma geométrica porque está asociada a detalles de suela.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Forma geométrica no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/marcas": {
            "get": {
                "tags": ["Marcas"],
                "summary": "Obtener todas las marcas registradas.",
                "description": "Este endpoint devuelve una lista de todas las marcas disponibles.",
                "responses": {
                    "200": {"description": "Lista de marcas.", "schema": {"type": "array", "items": {"$ref": "#/definitions/Marca"}}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "post": {
                "tags": ["Marcas"],
                "summary": "Crear una nueva marca.",
                "description": "Este endpoint permite crear una nueva marca con un nombre único.",
                "parameters": [
                    {
                        "in": "body",
                        "name": "marca",
                        "description": "Objeto de marca a crear.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nombre de la nueva marca."}
                            },
                            "required": ["nombre"]
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Marca creada exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "marca": {"$ref": "#/definitions/Marca"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (nombre requerido o duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/marcas/{id_marca}": {
            "get": {
                "tags": ["Marcas"],
                "summary": "Obtener una marca por su ID.",
                "description": "Este endpoint devuelve los detalles de una marca específica utilizando su ID.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_marca",
                        "type": "integer",
                        "required": True,
                        "description": "ID único de la marca a obtener."
                    }
                ],
                "responses": {
                    "200": {"description": "Detalles de la marca.", "schema": {"$ref": "#/definitions/Marca"}},
                    "404": {"description": "Marca no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "patch": {
                "tags": ["Marcas"],
                "summary": "Actualizar el nombre de una marca existente.",
                "description": "Este endpoint permite modificar el nombre de una marca específica. El nuevo nombre debe ser único.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_marca",
                        "type": "integer",
                        "required": True,
                        "description": "ID de la marca a actualizar."
                    },
                    {
                        "in": "body",
                        "name": "marca",
                        "description": "Objeto con el nuevo nombre de la marca.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nuevo nombre para la marca."}
                            },
                            "required": ["nombre"]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Marca actualizada exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "marca": {"$ref": "#/definitions/Marca"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (nombre requerido o duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Marca no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "delete": {
                "tags": ["Marcas"],
                "summary": "Eliminar una marca por su ID.",
                "description": "Este endpoint permite eliminar una marca específica, siempre y cuando no esté siendo utilizada por ningún calzado.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_marca",
                        "type": "integer",
                        "required": True,
                        "description": "ID de la marca a eliminar."
                    }
                ],
                "responses": {
                    "200": {"description": "Marca eliminada exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "No se puede eliminar la marca porque está asociada a calzados.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Marca no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/modelos": {
            "get": {
                "tags": ["Modelos"],
                "summary": "Obtener todos los modelos registrados.",
                "description": "Este endpoint devuelve una lista de todos los modelos disponibles.",
                "responses": {
                    "200": {"description": "Lista de modelos.", "schema": {"type": "array", "items": {"$ref": "#/definitions/Modelo"}}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "post": {
                "tags": ["Modelos"],
                "summary": "Crear un nuevo modelo.",
                "description": "Este endpoint permite crear un nuevo modelo con un nombre único.",
                "parameters": [
                    {
                        "in": "body",
                        "name": "modelo",
                        "description": "Objeto de modelo a crear.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nombre del nuevo modelo."}
                            },
                            "required": ["nombre"]
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Modelo creado exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "modelo": {"$ref": "#/definitions/Modelo"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (nombre requerido o duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/modelos/{id_modelo}": {
            "get": {
                "tags": ["Modelos"],
                "summary": "Obtener un modelo por su ID.",
                "description": "Este endpoint devuelve los detalles de un modelo específico utilizando su ID.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_modelo",
                        "type": "integer",
                        "required": True,
                        "description": "ID único del modelo a obtener."
                    }
                ],
                "responses": {
                    "200": {"description": "Detalles del modelo.", "schema": {"$ref": "#/definitions/Modelo"}},
                    "404": {"description": "Modelo no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "patch": {
                "tags": ["Modelos"],
                "summary": "Actualizar el nombre de un modelo existente.",
                "description": "Este endpoint permite modificar el nombre de un modelo específico. El nuevo nombre debe ser único.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_modelo",
                        "type": "integer",
                        "required": True,
                        "description": "ID del modelo a actualizar."
                    },
                    {
                        "in": "body",
                        "name": "modelo",
                        "description": "Objeto con el nuevo nombre del modelo.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nuevo nombre para el modelo."}
                            },
                            "required": ["nombre"]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Modelo actualizado exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "modelo": {"$ref": "#/definitions/Modelo"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (nombre requerido o duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Modelo no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "delete": {
                "tags": ["Modelos"],
                "summary": "Eliminar un modelo por su ID.",
                "description": "Este endpoint permite eliminar un modelo específico, siempre y cuando no esté siendo utilizada por ningún calzado.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_modelo",
                        "type": "integer",
                        "required": True,
                        "description": "ID del modelo a eliminar."
                    }
                ],
                "responses": {
                    "200": {"description": "Modelo eliminado exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "No se puede eliminar el modelo porque está asociado a calzados.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Modelo no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/categorias": {
            "get": {
                "tags": ["Categorías"],
                "summary": "Obtener todas las categorías registradas.",
                "description": "Este endpoint devuelve una lista de todas las categorías disponibles.",
                "responses": {
                    "200": {"description": "Lista de categorías.", "schema": {"type": "array", "items": {"$ref": "#/definitions/Categoria"}}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "post": {
                "tags": ["Categorías"],
                "summary": "Crear una nueva categoría.",
                "description": "Este endpoint permite crear una nueva categoría con un nombre único.",
                "parameters": [
                    {
                        "in": "body",
                        "name": "categoria",
                        "description": "Objeto de categoría a crear.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nombre de la nueva categoría."}
                            },
                            "required": ["nombre"]
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Categoría creada exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "categoria": {"$ref": "#/definitions/Categoria"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (nombre requerido o duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/categorias/{id_categoria}": {
            "get": {
                "tags": ["Categorías"],
                "summary": "Obtener una categoría por su ID.",
                "description": "Este endpoint devuelve los detalles de una categoría específica utilizando su ID.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_categoria",
                        "type": "integer",
                        "required": True,
                        "description": "ID único de la categoría a obtener."
                    }
                ],
                "responses": {
                    "200": {"description": "Detalles de la categoría.", "schema": {"$ref": "#/definitions/Categoria"}},
                    "404": {"description": "Categoría no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "patch": {
                "tags": ["Categorías"],
                "summary": "Actualizar el nombre de una categoría existente.",
                "description": "Este endpoint permite modificar el nombre de una categoría específica. El nuevo nombre debe ser único.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_categoria",
                        "type": "integer",
                        "required": True,
                        "description": "ID de la categoría a actualizar."
                    },
                    {
                        "in": "body",
                        "name": "categoria",
                        "description": "Objeto con el nuevo nombre de la categoría.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nuevo nombre para la categoría."}
                            },
                            "required": ["nombre"]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Categoría actualizada exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "categoria": {"$ref": "#/definitions/Categoria"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (nombre requerido o duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Categoría no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "delete": {
                "tags": ["Categorías"],
                "summary": "Eliminar una categoría por su ID.",
                "description": "Este endpoint permite eliminar una categoría específica, siempre y cuando no esté siendo utilizada por ningún calzado.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_categoria",
                        "type": "integer",
                        "required": True,
                        "description": "ID de la categoría a eliminar."
                    }
                ],
                "responses": {
                    "200": {"description": "Categoría eliminada exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "No se puede eliminar la categoría porque está asociada a calzados.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Categoría no encontrada.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/colores": {
            "get": {
                "tags": ["Colores"],
                "summary": "Obtener todos los colores registrados.",
                "description": "Este endpoint devuelve una lista de todos los colores disponibles.",
                "responses": {
                    "200": {"description": "Lista de colores.", "schema": {"type": "array", "items": {"$ref": "#/definitions/Color"}}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "post": {
                "tags": ["Colores"],
                "summary": "Crear un nuevo color.",
                "description": "Este endpoint permite crear un nuevo color con un nombre único.",
                "parameters": [
                    {
                        "in": "body",
                        "name": "color",
                        "description": "Objeto de color a crear.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nombre del nuevo color."}
                            },
                            "required": ["nombre"]
                        }
                    }
                ],
                "responses": {
                    "201": {
                        "description": "Color creado exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "color": {"$ref": "#/definitions/Color"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (nombre requerido o duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/colores/{id_color}": {
            "get": {
                "tags": ["Colores"],
                "summary": "Obtener un color por su ID.",
                "description": "Este endpoint devuelve los detalles de un color específico utilizando su ID.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_color",
                        "type": "integer",
                        "required": True,
                        "description": "ID único del color a obtener."
                    }
                ],
                "responses": {
                    "200": {"description": "Detalles del color.", "schema": {"$ref": "#/definitions/Color"}},
                    "404": {"description": "Color no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "patch": {
                "tags": ["Colores"],
                "summary": "Actualizar el nombre de un color existente.",
                "description": "Este endpoint permite modificar el nombre de un color específico. El nuevo nombre debe ser único.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_color",
                        "type": "integer",
                        "required": True,
                        "description": "ID del color a actualizar."
                    },
                    {
                        "in": "body",
                        "name": "color",
                        "description": "Objeto con el nuevo nombre del color.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nuevo nombre para el color."}
                            },
                            "required": ["nombre"]
                        }
                    }
                ],
                "responses": {
                    "200": {
                        "description": "Color actualizado exitosamente.",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "message": {"type": "string"},
                                "color": {"$ref": "#/definitions/Color"}
                            }
                        }
                    },
                    "400": {"description": "Error de validación (nombre requerido o duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Color no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "delete": {
                "tags": ["Colores"],
                "summary": "Eliminar un color por su ID.",
                "description": "Este endpoint permite eliminar un color específico, siempre y cuando no esté siendo utilizada por ningún calzado.",
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_color",
                        "type": "integer",
                        "required": True,
                        "description": "ID del color a eliminar."
                    }
                ],
                "responses": {
                    "200": {"description": "Color eliminado exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "No se puede eliminar el color porque está asociado a calzados.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Color no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/imputados": {
            "get": {
                "tags": ["Imputados"],
                "summary": "Obtener todos los imputados registrados.",
                "security": [{"JWT": []}],
                "responses": {
                    "200": {"description": "Lista de imputados.", "schema": {"type": "array", "items": {"$ref": "#/definitions/Imputado"}}},
                    "404": {"description": "No hay imputados registrados.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "post": {
                "tags": ["Imputados"],
                "summary": "Crear un nuevo imputado.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "body",
                        "name": "imputado",
                        "description": "Datos del imputado a crear.",
                        "required": True,
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string", "description": "Nombre del imputado."},
                                "apellido": {"type": "string", "description": "Apellido del imputado."},
                                "dni": {"type": "string", "description": "DNI del imputado."}
                            },
                            "required": ["nombre", "apellido", "dni"]
                        }
                    }
                ],
                "responses": {
                    "201": {"description": "Imputado creado exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "Datos inválidos (campos obligatorios faltantes o DNI duplicado).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        },
        "/imputados/{id_imputado}": {
            "get": {
                "tags": ["Imputados"],
                "summary": "Obtener un imputado por su ID.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_imputado",
                        "type": "integer",
                        "required": True,
                        "description": "ID único del imputado a obtener."
                    }
                ],
                "responses": {
                    "200": {"description": "Detalles del imputado.", "schema": {"$ref": "#/definitions/Imputado"}},
                    "404": {"description": "Imputado no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "patch": {
                "tags": ["Imputados"],
                "summary": "Actualizar parcialmente un imputado existente.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_imputado",
                        "type": "integer",
                        "required": True,
                        "description": "ID del imputado a actualizar."
                    },
                    {
                        "in": "body",
                        "name": "imputado",
                        "description": "Datos del imputado a actualizar (nombre, apellido, dni).",
                        "schema": {
                            "type": "object",
                            "properties": {
                                "nombre": {"type": "string"},
                                "apellido": {"type": "string"},
                                "dni": {"type": "string"}
                            },
                            "minProperties": 1
                        }
                    }
                ],
                "responses": {
                    "200": {"description": "Imputado actualizado exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "Datos inválidos (DNI duplicado o no se proporcionaron datos para actualizar).", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Imputado no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            },
            "delete": {
                "tags": ["Imputados"],
                "summary": "Eliminar un imputado por su ID.",
                "security": [{"JWT": []}],
                "parameters": [
                    {
                        "in": "path",
                        "name": "id_imputado",
                        "type": "integer",
                        "required": True,
                        "description": "ID del imputado a eliminar."
                    }
                ],
                "responses": {
                    "200": {"description": "Imputado eliminado exitosamente.", "schema": {"$ref": "#/definitions/MessageResponse"}},
                    "400": {"description": "No se puede eliminar el imputado porque está asociado a calzados.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "404": {"description": "Imputado no encontrado.", "schema": {"$ref": "#/definitions/ErrorResponse"}},
                    "500": {"description": "Error interno del servidor.", "schema": {"$ref": "#/definitions/ErrorResponse"}}
                }
            }
        }
    }
}