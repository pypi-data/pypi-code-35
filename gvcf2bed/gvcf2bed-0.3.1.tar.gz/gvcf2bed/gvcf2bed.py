"""
gvcf2bed tool
~~~~~~~~~~~~~


:copyright: (c) 2016 Sander Bollen
:copyright: (c) 2016 Leiden University Medical Center
:license: MIT
"""

import argparse
from collections import namedtuple
import vcf
import cyvcf2


class BedLine(namedtuple("BedLine", ["chromosome", "start", "end"])):

    def __str__(self):
        return "{0}\t{1}\t{2}".format(self.chromosome, self.start, self.end)


class BedGraphLine(namedtuple("BedGraphLine",
                              ["chromosome", "start", "end", "value"])):

    def __new__(cls, chromosome, start, end, value=0):
        return super(BedGraphLine, cls).__new__(
            cls,
            chromosome,
            start,
            end,
            value
        )

    def __str__(self):
        return "{0}\t{1}\t{2}\t{3}".format(
            self.chromosome,
            self.start,
            self.end,
            self.value
        )


def get_gqx(record, sample):
    """
    Get GQX value from a pyvcf record
    :param record: an instance of a pyvcf Record
    :param sample: sample name
    :return: float
    """
    fmt = record.genotype(sample)
    if hasattr(fmt.data, "GQ") and record.QUAL:
        return min(float(fmt.data.GQ), record.QUAL)
    elif hasattr(fmt.data, "GQ"):
        return float(fmt.data.GQ)
    elif record.QUAL:
        return record.QUAL
    else:
        return None


def get_gqx_cyvcf(record, sample_idx):
    """
    Get GQX value from a cyvcf2 record
    :param record: the record
    :param sample_idx: sample index
    :return: float
    """
    try:
        gq_arr = record.format("GQ")
    except KeyError:
        if record.QUAL is not None:
            return record.QUAL
        return None
    if record.QUAL is not None and gq_arr is not None:
        return min(float(gq_arr[sample_idx][0]), record.QUAL)
    elif gq_arr is not None:
        return gq_arr[sample_idx][0]
    elif record.QUAL is not None:
        return record.QUAL
    else:
        return None


def is_variant(record):
    """
    Return true if record is a variant
    Standard pyvcf `.is_snp` does not work correctly for
    GATK's GVCF format
    :param record: pyvcf record
    :return:
    """
    alts = set(list(map(str, record.ALT)))
    non_variant_alts = {".", "<NON_REF>"}
    true_alts = alts - non_variant_alts
    return len(true_alts) >= 1


def vcf_record_to_bed(record, bedgraph=False, val=0):
    """
    Convert a VCF record to a BED record
    :param record: vcf record
    :param bedgraph: output BedGraphLine records in stead of BedLine
    :param val: value to output if bedgraph=True
    :return: BedLine record
    """
    if "END" in record.INFO:
        if bedgraph:
            return BedGraphLine(record.CHROM, record.start,
                                record.INFO['END'], val)
        return BedLine(record.CHROM, record.start, record.INFO['END'])
    if bedgraph:
        return BedGraphLine(record.CHROM, record.start, record.end, val)
    return BedLine(record.CHROM, record.start, record.end)


def main():
    desc = """
    Create a BED file from a gVCF.
    Regions are based on a minimum genotype quality.
    The gVCF file must contain a GQ field in its FORMAT fields.

    GQ scores of non-variants records have a different distribution
    from the GQ score distribution of variant records.
    Hence, an option is provided to set a different threshold for
    non-variant positions.
    """
    parser = argparse.ArgumentParser(description=desc)

    parser.add_argument("-I", "--input", type=str,
                        required=True, help="Input gVCF")
    parser.add_argument("-O", "--output", type=str,
                        required=True, help="Output bed file")
    parser.add_argument("-s", "--sample", type=str,
                        required=False,
                        help="Sample name in VCF file to use. "
                             "Will default to first sample "
                             "(alphabetically) if not supplied")
    parser.add_argument("-q", "--quality", type=int, default=20,
                        help="Minimum genotype quality (default 20)")
    parser.add_argument("-nq", "--non-variant-quality", type=int, default=20,
                        help="Minimum genotype quality for "
                             "non-variant records (default 20)")

    parser.add_argument("-b", "--bedgraph", action="store_true",
                        help="Output in bedgraph mode")

    args = parser.parse_args()

    reader = cyvcf2.VCF(args.input)
    if not args.sample:
        sample = 0
    else:
        sample = reader.samples.index(args.sample)

    with open(args.output, "w") as ohandle:
        for record in reader:
            gq = get_gqx_cyvcf(record, sample)
            if gq is None:
                continue
            is_v = is_variant(record)
            if (is_v and gq >= args.quality) or \
                    (not is_v and gq >= args.non_variant_quality):
                ohandle.write(str(vcf_record_to_bed(
                    record,
                    args.bedgraph,
                    gq
                )) + "\n")


if __name__ == "__main__":
    main()
