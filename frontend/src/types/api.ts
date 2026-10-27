// TypeScript types for AgroVision-Mine API

export interface HealthResponse {
  status: string
  platform: string
  dataset_version: string
  records_count: number
  manifest_sha256_verified: boolean
  features_sha256_verified: boolean
}

export interface CropCount {
  crop: string
  count: number
  percentage: number
}

export interface OverviewResponse {
  corpus_size: number
  taxa_count: number
  top_crops: CropCount[]
  pathological_status: {
    diseased: number
    healthy: number
    diseased_percentage: number
    healthy_percentage: number
  }
  sources: {
    plantdoc: number
    plantdoc_percentage: number
    icar_ogd: number
    icar_ogd_percentage: number
  }
  feature_dimensions: {
    continuous_count: number
    groups: string
    normalization: string
  }
  clustering_summary: {
    metric_supported_k: number
    k2_silhouette: number
    k4_silhouette: number
    pca_variance_explained: number
  }
  association_summary: {
    mode_a_visual_rules: number
    mode_b_labeled_rules: number
    rule_parity_rate: string
  }
  verification_status: {
    frozen_manifest_sha256: string
    frozen_features_sha256: string
    verified: boolean
  }
}

export interface DatasetRecord {
  image_id: string
  filename: string
  crop_name: string
  disease_name: string
  condition_status: string
  pathogen_type: string
  is_pest: boolean
  dataset_source: string
  dominant_color_tone: string
  cluster_id_k2?: number | null
  cluster_id_k4?: number | null
  pca_x?: number | null
  pca_y?: number | null
  has_image: boolean
}

export interface DatasetResponse {
  total_records: number
  page: number
  page_size: number
  total_pages: number
  records: DatasetRecord[]
  filter_options: {
    crops: string[]
    conditions: string[]
    pathogens: string[]
    sources: string[]
  }
}

export interface SpecimenDetail {
  image_id: string
  filename: string
  crop_label: string
  condition_label: string
  disease_label: string
  pathogen_type: string
  is_pest: boolean
  dominant_color_tone: string
  cluster_id_k2?: number | null
  cluster_id_k4?: number | null
  pca_coordinates: {
    x?: number | null
    y?: number | null
  }
  color_features: Record<string, number>
  glcm_features: Record<string, number>
  shape_features: Record<string, number>
  image_exists: boolean
  image_url: string
}

export interface TableColumn {
  cid: number
  name: string
  type: string
  notnull: boolean
  primary_key: boolean
}

export interface TableInfo {
  table_name: string
  table_type: string
  row_count: number
  columns: TableColumn[]
}

export interface WarehouseSchemaResponse {
  database_type: string
  database_path: string
  tables: TableInfo[]
  relationships: Array<{ from: string; to: string }>
}

export interface OLAPOperation {
  id: string
  name: string
  description: string
}

export interface OLAPMetadataResponse {
  dimensions: Array<{
    name: string
    levels: string[]
    selectable_values: string[]
  }>
  measures: Array<{
    name: string
    label: string
    type: string
  }>
  operations: OLAPOperation[]
}

export interface OLAPQueryResponse {
  operation: string
  hierarchy: string
  sql: string
  row_count: number
  latency_ms: number
  columns: string[]
  data: Record<string, any>[]
}

export interface PCAPoint {
  image_id: string
  crop: string
  disease: string
  condition: string
  cluster: number
  x: number
  y: number
}

export interface ClusteringResponse {
  metric_supported_k: number
  exploratory_subpartition_k: number
  selected_k: number
  is_metric_optimal: boolean
  k_selection_rationale: string
  multi_k_evaluation: Array<{
    k: number
    silhouette_score: number
    davies_bouldin_index: number
    calinski_harabasz_score: number
    inertia: number
  }>
  pca_projection: {
    explained_variance_ratio: number[]
    total_variance_explained: number
  }
  solution_metrics: {
    k: number
    silhouette_score: number
    davies_bouldin_score?: number
    davies_bouldin_index?: number
    calinski_harabasz_score: number
    cluster_sizes: Record<string, number>
  }
  cluster_profiles: Array<{
    cluster_id: number
    size: number
    percentage: number
    top_elevated_features: Array<{ feature: string; cluster_mean: number; global_mean: number; z_score: number }>
    top_suppressed_features: Array<{ feature: string; cluster_mean: number; global_mean: number; z_score: number }>
  }>
  contingency_analysis: Record<string, any>
  scientific_findings: string[]
  scatter_points: PCAPoint[]
}

export interface AssociationRule {
  antecedents: string[]
  consequents: string[]
  support: number
  confidence: number
  lift: number
}

export interface AssociationRulesResponse {
  mode: string
  mode_id: string
  methodological_warning?: string | null
  total_rules: number
  total_filtered_rules?: number
  total_generated_rules?: number
  active_filters?: {
    min_support: number
    min_confidence: number
    min_lift: number
    search?: string | null
  }
  page: number
  page_size: number
  total_pages: number
  rules: AssociationRule[]
  algorithm_benchmark: any
  scientific_advisory: {
    title: string
    principle: string
    discretization: string
  }
}

export interface PredictionCandidate {
  rank: number
  composite_class: string
  label: string
  crop_name: string
  disease_name: string
  condition_status: string
  probability: number
  probability_percent: number
  raw_logit: number
}

export interface SupervisedPredictionResult {
  status: 'confident' | 'uncertain'
  is_uncertain: boolean
  uncertainty_reason?: string | null
  predicted_class: string
  predicted_label: string
  crop_name: string
  disease_name: string
  condition_status: string
  confidence_score: number
  confidence_percent: number
  raw_logit: number
  prediction_entropy: number
  normalized_entropy: number
  top_candidates: PredictionCandidate[]
  model_metadata: {
    architecture: string
    pretrained_origin: string
    input_resolution: string
    supported_classes_count: number
    benchmark_sample_size: number
    test_macro_f1: number
    test_accuracy: number
    test_ci_95: [number, number]
    confidence_threshold: number
  }
  scientific_advisory: {
    interpretation: string
    nearest_reference_separation: string
  }
}

export interface NearestSpecimen {
  rank: number
  image_id: string
  crop_name: string
  disease_name: string
  condition_status: string
  pathogen_type: string
  dataset_source: string
  euclidean_distance: number
  visual_similarity_score: number
  is_self_match?: boolean
  image_url: string
}

export interface ImageAnalysisResponse {
  prediction?: SupervisedPredictionResult | null
  validation: {
    is_valid: boolean
    filename: string
    format: string
    raw_width: number
    raw_height: number
    channels: number
    file_size_kb: number
    blur_score: number
    is_blurry: boolean
    color_space: string
    original_color_mode?: string
    exif_orientation_corrected?: boolean
    processed_width: number
    processed_height: number
  }
  dominant_color_tone: string
  feature_counts: {
    color_moments: number
    glcm_texture: number
    contour_morphology: number
    total_continuous_features: number
  }
  features_grouped: {
    color: Record<string, number>
    texture: Record<string, number>
    shape: Record<string, number>
  }
  features_grouped_raw?: {
    color: Record<string, number>
    texture: Record<string, number>
    shape: Record<string, number>
  }
  features_grouped_standardized?: {
    color: Record<string, number>
    texture: Record<string, number>
    shape: Record<string, number>
  }
  features_raw: Record<string, number>
  features_standardized?: Record<string, number>
  feature_definitions?: Record<string, {
    name: string
    category: string
    range: string
    description: string
  }>
  clustering: {
    k2: {
      cluster_id: number
      designation: string
      characteristics: string
    }
    k4: {
      cluster_id: number
      designation: string
      characteristics: string
    }
  }
  pca_projection: {
    x: number
    y: number
    pc1_explained_pct: number
    pc2_explained_pct: number
    total_explained_pct: number
  }
  nearest_specimens: NearestSpecimen[]
  diagnostic_interpretation?: {
    status: string
    message: string
    notice: string
    majority_label_warning: string
    supervised_classifier: string
  }
  repository_distribution?: {
    total: number
    diseased: number
    healthy: number
    diseased_pct: number
    healthy_pct: number
  }
  scientific_caveats: {
    disease_classification: string
    classification_disclosure: string
    distance_vs_probability: string
    warehouse_integrity_guarantee: string
  }
}
