export interface Scenario {
  id: string;
  title: string;
  subtitle: string;
  sender: string;
  subject: string;
  body: string;
  image_b64: string | null;
  expected_route: string;
}

export interface PipelineStep {
  name: string;
  status: 'executed' | 'skipped';
  description: string;
}

export interface CrossAttentionTokenPair {
  text_token: string;
  image_token: string;
  strength: number;
}

export interface InferenceResult {
  email_id: string;
  modality: 'text' | 'image' | 'multimodal' | 'empty';
  has_text: boolean;
  has_meaningful_image: boolean;
  text_length: number;
  image_count: number;
  filtered_image_count: number;
  pipeline_steps: PipelineStep[];
  simulated_spam_probability: number;
  simulated_label: 'SPAM' | 'LEGITIMATE';
  detected_signals: {
    text: string[];
    image: string[];
    crossmodal: string[];
  };
  cross_attention_pairs: CrossAttentionTokenPair[];
  explanation: string;
  computation_saved_description: string;
  is_demo_simulation: boolean;
}
