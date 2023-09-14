CREATE TABLE Block (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    Chain_ID INT REFERENCES Blockchain(ID),
    Block_Number BIGINT NOT NULL,
    Parent_Hash VARCHAR(255) NOT NULL,
    Block_Timestamp BIGINT NOT NULL,
    Transaction_Count INT NOT NULL
);
