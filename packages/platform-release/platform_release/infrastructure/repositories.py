from sqlalchemy.orm import Session
from platform_release.infrastructure.database.models import (
    DBPlatformBaseline,
    DBCertificationReport,
    DBContractVersionMatrix,
    DBDocumentationIndex,
    DBReleaseManifest
)
from typing import Optional

class ReleaseRepository:
    def __init__(self, db: Session):
        self.db = db

    def save_baseline(self, baseline: DBPlatformBaseline):
        self.db.add(baseline)
        self.db.commit()

    def get_baseline_by_version(self, version: str) -> Optional[DBPlatformBaseline]:
        return self.db.query(DBPlatformBaseline).filter(DBPlatformBaseline.version == version).first()

    def save_certification(self, cert: DBCertificationReport):
        self.db.add(cert)
        self.db.commit()

    def get_certification_by_version(self, version: str) -> Optional[DBCertificationReport]:
        return self.db.query(DBCertificationReport).filter(DBCertificationReport.version == version).first()

    def save_contract_matrix(self, matrix: DBContractVersionMatrix):
        self.db.add(matrix)
        self.db.commit()

    def get_contract_matrix_by_version(self, version: str) -> Optional[DBContractVersionMatrix]:
        return self.db.query(DBContractVersionMatrix).filter(DBContractVersionMatrix.version == version).first()

    def save_documentation_index(self, doc_index: DBDocumentationIndex):
        self.db.add(doc_index)
        self.db.commit()

    def get_documentation_index_by_version(self, version: str) -> Optional[DBDocumentationIndex]:
        return self.db.query(DBDocumentationIndex).filter(DBDocumentationIndex.version == version).first()

    def save_release_manifest(self, manifest: DBReleaseManifest):
        self.db.add(manifest)
        self.db.commit()

    def get_release_manifest(self, version: str) -> Optional[DBReleaseManifest]:
        return self.db.query(DBReleaseManifest).filter(DBReleaseManifest.version == version).first()
