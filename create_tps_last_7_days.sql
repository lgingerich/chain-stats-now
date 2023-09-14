CREATE TABLE tps_last_7_days (
    ID SERIAL PRIMARY KEY,
    Chain_ID INT REFERENCES Blockchain(Chain_ID),
    Block_Timestamp BIGINT NOT NULL,
    TPS_Min FLOAT NOT NULL,
    TPS_Avg FLOAT NOT NULL,
    TPS_Max FLOAT NOT NULL,
    UNIQUE (Chain_ID, Block_Timestamp)
);
