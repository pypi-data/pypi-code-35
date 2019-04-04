#!/usr/bin/env python
# -*- coding: UTF-8 -*-
# Created by Roberto Preste
import asyncio
from apybiomart.dataset import Dataset


async def query_dataset(chromosome):
    dataset = Dataset(name="hsapiens_gene_ensembl",
                      host="http://www.ensembl.org")
    print("starting query for {}".format(chromosome))
    await dataset.query(attributes=["ensembl_gene_id", "external_gene_name"],
                        filters={"chromosome_name": chromosome})
    print("executed query for {}".format(chromosome))
    return


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    # tasks = [query_dataset(str(i)) for i in range(5)]
    # loop.run_until_complete(asyncio.gather(*tasks))
    loop.run_until_complete(query_dataset("1"))

