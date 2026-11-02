-- Run once as MySQL administrator against pharmacy_database.
-- SupplierMedication references SupplierID, so remove its foreign key briefly.
ALTER TABLE SupplierMedication
    DROP FOREIGN KEY fk_suppliermed_supplier;

-- MySQL now assigns the next SupplierID when the form inserts a supplier.
ALTER TABLE Supplier
    MODIFY SupplierID INT UNSIGNED NOT NULL AUTO_INCREMENT;

-- Restore the original relationship between suppliers and medications.
ALTER TABLE SupplierMedication
    ADD CONSTRAINT fk_suppliermed_supplier
    FOREIGN KEY (SupplierID) REFERENCES Supplier (SupplierID);
