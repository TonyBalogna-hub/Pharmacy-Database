-- Run this once as the MySQL administrator.
-- It lets MySQL choose SupplierID when a supplier is added.
ALTER TABLE Supplier
    MODIFY SupplierID INT UNSIGNED NOT NULL AUTO_INCREMENT;
