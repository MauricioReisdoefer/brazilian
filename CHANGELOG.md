# Changelog

Todas as mudanças relevantes neste projeto serão documentadas aqui.

O formato segue as recomendações de **Keep a Changelog**  
e este projeto utiliza **Semantic Versioning (SemVer)**.

---

## v1.1.1

Consertamos o Date SQLAlchemy type. O `process_bind_param` retornava incorretamente.

---

## v1.1.2

Consertamos o Time SQLAlchemy type. O `process_bind_param` retornava incorretamente.

---

## v1.1.3

Refatorados todos os tipos Pydantic para aceitarem tanto strings quanto instâncias já validadas das classes correspondentes.
