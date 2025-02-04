<!-- markdownlint-disable first-line-h1 -->
<div class="float-img">
  <img src="../../assets/operation-bcd.png" alt="Operation group in BCD explorer">
  <img src="../../assets/operation-config.png" alt="`operation` index config">
</div>

# `operation` index

Operation index allows you to query only operations related to your dapp and match them with handlers by content. A single contract call consists of implicit operation and, optionally, internal operations. For each of them, you can specify a handler that will be called when the operation group matches. As a result, you get something like an event log for your dapp.

## Handlers

Each operation handler contains two required fields:

* `callback` — a name of async function with a particular signature; DipDup will search for it in `<package>.handlers.<callback>` module.
* `pattern` — a non-empty list of items that need to be matched.

```yaml
indexes:
  my_index:
    kind: operation
    datasource: tzkt
    contracts:
      - some_contract
    handlers:
      - callback: on_call
        pattern:
          - destination: some_contract
            entrypoint: transfer
```

You can think of the operation pattern as a regular expression on a sequence of operations (both external and internal) with a global flag enabled (there can be multiple matches). Multiple operation parameters can be used for matching (source, destination, etc.).

You will get slightly different callback argument types depending on whether pattern item is typed or not. If so, DipDup will generate the dataclass for a particular entrypoint/storage, otherwise you will have to handle untyped parameters/storage updates stored in `OperationData` model.

## Matching originations

| name                            | description                                                                                                                            | supported | typed |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- |:---------:|:-----:|
| `originated_contract.address`   | Origination of exact contract.                                                                                                         |     ✅     |   ✅   |
| `originated_contract.code_hash` | Originations of all contracts having the same code.                                                                                    |     ✅     |   ✅   |
| `source.address`                | Special cases only. This filter is very slow and doesn't support strict typing. Usually, `originated_contract.code_hash` suits better. |     ⚠     |   ❌   |
| `source.code_hash`              | Currently not supported.                                                                                                               |     ❌     |   ❌   |
| `similar_to.address`            | Compatibility alias to `originated_contract.code_hash`. Can be removed some day.                                                       |     ➡️    |   ➡️  |
| `similar_to.code_hash`          | Compatibility alias to `originated_contract.code_hash`. Can be removed some day.                                                       |     ➡️    |   ➡️  |

## Matching transactions

| name                     | description                                | supported | typed |
| ------------------------ | ------------------------------------------ |:---------:|:-----:|
| `source.address`         | Sent by exact address.                     |     ✅     |  N/A  |
| `source.code_hash`       | Sent by any contract having this code hash |     ✅     |  N/A  |
| `destination.address`    | Invoked contract address                   |     ✅     |   ✅   |
| `destination.code_hash`  | Invoked contract code hash                 |     ✅     |   ✅   |
| `destination.entrypoint` | Entrypoint called                          |     ✅     |   ✅   |

## Optional items

Pattern items have `optional` field to continue matching even if this item is not found. It's usually unnecessary to match the entire operation content; you can skip external/internal calls that are not relevant. However, there is a limitation: optional items cannot be followed by operations ignored by the pattern.

```yaml
pattern:
  # Implicit transaction
  - destination: some_contract
    entrypoint: mint

  # Internal transactions below
  - destination: another_contract
    entrypoint: transfer

  - source: some_contract
    type: transaction
```

## Specifying contracts to index

DipDup will try to guess the list of used contracts by handlers' signatures. If you want to specify it explicitly, use `contracts` field:

```yaml
indexes:
  my_index:
    kind: operation
    datasource: tzkt
    contracts:
      - foo
      - bar
```

## Specifying operation types

By default, DipDup processes only transactions, but you can enable other operation types you want to process (currently, `transaction`, `origination`, and `migration` are supported).

```yaml
indexes:
  my_index:
    kind: operation
    datasource: tzkt
    types:
      - transaction
      - origination
      - migration
```
