ALTER TABLE IF EXISTS dipdup_token_metadata DROP CONSTRAINT dipdup_token_metadata_pkey;
ALTER TABLE IF EXISTS dipdup_token_metadata ADD PRIMARY KEY (contract, token_id);