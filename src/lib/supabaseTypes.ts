export type Json = string | number | boolean | null | { [key: string]: Json | undefined } | Json[];

export type Database = {
    public: {
        Tables: {
            cells: {
                Row: {
                    content: string;
                    created_at: string;
                    id: string;
                    metadata: Json | null;
                    notebook: string;
                    type: string;
                };
                Insert: {
                    content: string;
                    created_at?: string;
                    id?: string;
                    metadata?: Json | null;
                    notebook: string;
                    type?: string;
                };
                Update: {
                    content?: string;
                    created_at?: string;
                    id?: string;
                    metadata?: Json | null;
                    notebook?: string;
                    type?: string;
                };
                Relationships: [
                    {
                        foreignKeyName: 'public_cells_notebook_fkey';
                        columns: ['notebook'];
                        isOneToOne: false;
                        referencedRelation: 'notebooks';
                        referencedColumns: ['id'];
                    },
                ];
            };
            countries: {
                Row: {
                    continent: Database['public']['Enums']['continents'] | null;
                    id: number;
                    iso2: string;
                    iso3: string | null;
                    local_name: string | null;
                    name: string | null;
                };
                Insert: {
                    continent?: Database['public']['Enums']['continents'] | null;
                    id?: number;
                    iso2: string;
                    iso3?: string | null;
                    local_name?: string | null;
                    name?: string | null;
                };
                Update: {
                    continent?: Database['public']['Enums']['continents'] | null;
                    id?: number;
                    iso2?: string;
                    iso3?: string | null;
                    local_name?: string | null;
                    name?: string | null;
                };
                Relationships: [];
            };
            llm_runs: {
                Row: {
                    context: string | null;
                    created_at: string;
                    id: string;
                    prompt: string | null;
                    response: string | null;
                    sources: Json | null;
                };
                Insert: {
                    context?: string | null;
                    created_at?: string;
                    id?: string;
                    prompt?: string | null;
                    response?: string | null;
                    sources?: Json | null;
                };
                Update: {
                    context?: string | null;
                    created_at?: string;
                    id?: string;
                    prompt?: string | null;
                    response?: string | null;
                    sources?: Json | null;
                };
                Relationships: [];
            };
            notebooks: {
                Row: {
                    created_at: string;
                    created_by: string;
                    id: string;
                    name: string | null;
                    notes: Json | null;
                    public: boolean | null;
                    shared: string[] | null;
                };
                Insert: {
                    created_at?: string;
                    created_by?: string;
                    id?: string;
                    name?: string | null;
                    notes?: Json | null;
                    public?: boolean | null;
                    shared?: string[] | null;
                };
                Update: {
                    created_at?: string;
                    created_by?: string;
                    id?: string;
                    name?: string | null;
                    notes?: Json | null;
                    public?: boolean | null;
                    shared?: string[] | null;
                };
                Relationships: [
                    {
                        foreignKeyName: 'public_notebooks_created_by_fkey';
                        columns: ['created_by'];
                        isOneToOne: false;
                        referencedRelation: 'users';
                        referencedColumns: ['id'];
                    },
                ];
            };
        };
        Views: {
            [_ in never]: never;
        };
        Functions: {
            [_ in never]: never;
        };
        Enums: {
            continents: 'Africa' | 'Antarctica' | 'Asia' | 'Europe' | 'Oceania' | 'North America' | 'South America';
        };
        CompositeTypes: {
            [_ in never]: never;
        };
    };
};

export type Tables<
    PublicTableNameOrOptions extends
        | keyof (Database['public']['Tables'] & Database['public']['Views'])
        | { schema: keyof Database },
    TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
        ? keyof (Database[PublicTableNameOrOptions['schema']]['Tables'] &
              Database[PublicTableNameOrOptions['schema']]['Views'])
        : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
    ? (Database[PublicTableNameOrOptions['schema']]['Tables'] &
          Database[PublicTableNameOrOptions['schema']]['Views'])[TableName] extends {
          Row: infer R;
      }
        ? R
        : never
    : PublicTableNameOrOptions extends keyof (Database['public']['Tables'] & Database['public']['Views'])
      ? (Database['public']['Tables'] & Database['public']['Views'])[PublicTableNameOrOptions] extends {
            Row: infer R;
        }
          ? R
          : never
      : never;

export type TablesInsert<
    PublicTableNameOrOptions extends keyof Database['public']['Tables'] | { schema: keyof Database },
    TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
        ? keyof Database[PublicTableNameOrOptions['schema']]['Tables']
        : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
    ? Database[PublicTableNameOrOptions['schema']]['Tables'][TableName] extends {
          Insert: infer I;
      }
        ? I
        : never
    : PublicTableNameOrOptions extends keyof Database['public']['Tables']
      ? Database['public']['Tables'][PublicTableNameOrOptions] extends {
            Insert: infer I;
        }
          ? I
          : never
      : never;

export type TablesUpdate<
    PublicTableNameOrOptions extends keyof Database['public']['Tables'] | { schema: keyof Database },
    TableName extends PublicTableNameOrOptions extends { schema: keyof Database }
        ? keyof Database[PublicTableNameOrOptions['schema']]['Tables']
        : never = never,
> = PublicTableNameOrOptions extends { schema: keyof Database }
    ? Database[PublicTableNameOrOptions['schema']]['Tables'][TableName] extends {
          Update: infer U;
      }
        ? U
        : never
    : PublicTableNameOrOptions extends keyof Database['public']['Tables']
      ? Database['public']['Tables'][PublicTableNameOrOptions] extends {
            Update: infer U;
        }
          ? U
          : never
      : never;

export type Enums<
    PublicEnumNameOrOptions extends keyof Database['public']['Enums'] | { schema: keyof Database },
    EnumName extends PublicEnumNameOrOptions extends { schema: keyof Database }
        ? keyof Database[PublicEnumNameOrOptions['schema']]['Enums']
        : never = never,
> = PublicEnumNameOrOptions extends { schema: keyof Database }
    ? Database[PublicEnumNameOrOptions['schema']]['Enums'][EnumName]
    : PublicEnumNameOrOptions extends keyof Database['public']['Enums']
      ? Database['public']['Enums'][PublicEnumNameOrOptions]
      : never;
