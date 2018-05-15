
CREATE TABLE category (
    category_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    category_name VARCHAR(128) NOT NULL,
    link_openfoodfacts VARCHAR(500),
    PRIMARY KEY (category_id)
);


CREATE TABLE product (
    product_id SMALLINT UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    product_name VARCHAR(128) NOT NULL,
    category_id SMALLINT UNSIGNED NOT NULL,
    product_brand VARCHAR(128),
    nutriscore SMALLINT UNSIGNED NOT NULL,
    description TEXT,
    store VARCHAR(200),
    link_openfoodfacts VARCHAR(500),
    saved BOOL,
    CONSTRAINT fk_category_id
        FOREIGN KEY (category_id)
        REFERENCES category(category_id)
);

