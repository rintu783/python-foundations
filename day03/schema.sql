CREATE TABLE IF NOT EXISTS people(
    id       SERIAL PRIMARY KEY,
    name     TEXT NOT NULL UNIQUE,
    balance  NUMERIC(12,2) NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS expenses(
    id          SERIAL PRIMARY KEY,
    description TEXT NOT NULL,
    amount      NUMERIC(12,2) NOT NULL,
    paid_by     INTEGER NOT NULL REFERENCES people(id),
    created_at  TIMESTAMP NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS expense_shares(
    id          SERIAL PRIMARY KEY,
    expense_id  INTEGER NOT NULL REFERENCES expenses(id) ON DELETE CASCADE,
    person_id   INTEGER NOT NULL REFERENCES people(id),
    share       NUMERIC(12,2) NOT NULL
);
